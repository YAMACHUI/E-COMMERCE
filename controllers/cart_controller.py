from flask import jsonify, request
from services.cart_service import CartService

class CartController:
    @staticmethod
    def add_item(session):
        data = request.get_json()
        cart_service = CartService(session)
        
        try:
            cart = cart_service.add_to_cart(
                user_id=data['user_id'],
                product_id=data['product_id'],
                stock_quantity=data.get('stock_quantity', 1)
            )
            return jsonify({
            "message": "Produit ajouté au panier",
            "cart_id": cart.id,
            "remaining_stock": cart_service.get_product_stock(data['product_id'])
        }), 200

        except ValueError as e:
            return jsonify({"error": str(e)}), 400
        except Exception as e:
            return jsonify({"error": "Une erreur est survenue"}), 500

    @staticmethod
    def remove_item(session):
        data = request.get_json()
        cart_service = CartService(session)
        
        try:
            cart = cart_service.remove_from_cart(
                user_id=data['user_id'],
                product_id=data['product_id']
            )
            return jsonify({"message": "Produit retiré du panier"}), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 400

@staticmethod
def get_cart(session, user_id=None):
    try:
        # Initialisation systématique du service
        cart_service = CartService(session)
        
        # Si user_id n'est pas fourni, le récupérer de la requête
        if user_id is None:
            user_id = request.args.get('user_id')
            if not user_id:
                return jsonify({"error": "user_id manquant"}), 400

        # Récupération du panier
        cart = cart_service.get_user_cart(user_id)
        if not cart:
            return jsonify({"message": "Panier vide"}), 200
            
        # Construction de la réponse
        items = [{
            "product_id": item.product_id,
            "stock_quantity": item.stock_quantity,
            "product_name": item.product.name,
            "price": item.product.price
        } for item in cart.items]
        
        return jsonify({
            "cart_id": cart.id,
            "user_id": cart.user_id,
            "items": items,
            "total": sum(item.product.price * item.stock_quantity for item in cart.items)
        }), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 400