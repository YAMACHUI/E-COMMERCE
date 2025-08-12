from models.cart import Cart, CartItem
from sqlalchemy.orm import Session
from models.product import Product
from flask import Flask,request,jsonify
class CartService:
    def __init__(self, db_session: Session):
        self.db = db_session

    def get_user_cart(self, user_id: int):
        return self.db.query(Cart).filter_by(user_id=user_id).first()

    def add_to_cart(self, user_id: int, product_id: int, stock_quantity: int = 1):
            # Récupérer le produit
            product = self.db.query(Product).get(product_id)
            if not product:
                raise ValueError("Produit non trouvé")
            
            # Validation du stock
            if stock_quantity <= 0:
                raise ValueError("La quantité doit être supérieure à zéro")
                
              # Vérification améliorée du stock
            if stock_quantity > product.stock_quantity:
                raise ValueError(
                    f"Quantité demandée trop élevée. Vous avez demandé {stock_quantity} unités "
                    f"mais seulement {product.stock_quantity} sont disponibles"
                )
            
            # Gestion du panier
            cart = self.get_user_cart(user_id)
            if not cart:
                cart = Cart(user_id=user_id)
                self.db.add(cart)
                self.db.commit()

            item = self.db.query(CartItem).filter_by(cart_id=cart.id, product_id=product_id).first()
            if item:
                # Vérification du stock pour la quantité cumulée
                new_quantity = item.stock_quantity + stock_quantity
                if new_quantity > product.stock_quantity:
                    raise ValueError(
                f"Quantité totale trop élevée. Votre panier contient déjà {item.stock_quantity} unités "
                f"et vous en ajoutez {stock_quantity}, mais seulement {product.stock_quantity} sont disponibles"
            )
                item.stock_quantity = new_quantity
            else:
                item = CartItem(cart_id=cart.id, product_id=product_id, stock_quantity=stock_quantity)
                self.db.add(item)
            
            self.db.commit()
            return cart

    def remove_from_cart(self, user_id: int, product_id: int):
        cart = self.get_user_cart(user_id)
        if cart:
            item = self.db.query(CartItem).filter_by(cart_id=cart.id, product_id=product_id).first()
            if item:
                self.db.delete(item)
                self.db.commit()
        return cart

    def clear_cart(self, user_id: int):
        cart = self.get_user_cart(user_id)
        if cart:
            self.db.query(CartItem).filter_by(cart_id=cart.id).delete()
            self.db.commit()
        return cart
    
    def get_product_stock(self, product_id: int):
        product = self.db.query(Product).get(product_id)
        return product.stock_quantity if product else 0
    
    @staticmethod
    def get_cart(session, user_id=None):
     try:
        # Initialisation systématique du service
        cart_service = CartService(session)
        
        # Récupération du user_id si non fourni
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
            "total": sum(item['price'] * item['stock_quantity'] for item in items)
        }), 200
        
     except Exception as e:
        return jsonify({"error": str(e)}), 400