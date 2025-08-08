from flask import jsonify, request
from services.product_service import ProductService
from Validator.product_validator import ProductValidator 
class ProductController:

    @staticmethod
    def get_all_products(service: ProductService):
        try:
            products = service.get_all_products_by_price_desc()
            return jsonify([{
                'product_id': p.product_id,
                'name': p.name,
                'description': p.description,
                'sku': p.sku,
                'price': p.price,
                'stock_quantity': p.stock_quantity,
                'category_id': p.category_id
            } for p in products])
        except Exception as e:
            return jsonify({'error': 'Erreur interne lors de la récupération'}), 500


    @staticmethod
    def create_product(session):
        product_service = ProductService(session)
        data = request.get_json()
        
        is_valid, error_msg = ProductValidator.validate_create(data)
        if not is_valid:
           return jsonify({"error": error_msg}), 400

        try:
            new_product = product_service.create_product(
                name=data['name'],
                price=data['price'],
                sku=data['sku'],
                description=data.get('description'),
                stock_quantity=data.get('stock_quantity', 0),
                category_id=data.get('category_id')
            )
            return jsonify(new_product), 201

        except ValueError as e:
            return jsonify({"error": str(e)}), 400
        except Exception as e:
            return jsonify({"error": "Erreur interne du serveur"}), 500