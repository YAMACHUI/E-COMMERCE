from flask import Flask,request,jsonify
from sqlalchemy import create_engine,inspect
from sqlalchemy.orm import sessionmaker,scoped_session
from models.product import Product
from models.base import Base
from services.product_service import ProductService
from services.category_service import CategoryService
from services.user_service import UserService
from controllers.product_controller import ProductController
from controllers.category_controller import CategoryController
from controllers.user_controller import UserController
from models.category import Category
from utils.response import ApiResponse
from Validator.product_validator import ProductValidator
from models.user import User
from controllers.user_controller import UserController
from controllers.auth_controller import AuthController
from datetime import timedelta
from sqlalchemy import desc
from flask_jwt_extended import (
    JWTManager,
    jwt_required,
    create_access_token,
    create_refresh_token,
    get_jwt_identity, 
    get_jwt)
from utils.auth_utils import admin_required,toto

app=Flask(__name__)
app.config['JWT_SECRET_KEY']= 'votre_cle_secrete_tres_complex' # À changer en production
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(minutes=30) 
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(days=1)

jwt = JWTManager(app)

db_url="postgresql+psycopg2://postgres:YAMACHUI@localhost:2006/e-commerce"

engine = create_engine(db_url)
Session = scoped_session(sessionmaker(bind=engine))

# Création des tables 
{
    "name": "Smartphone X",
    "price": 799.99,
    "sku": "SMX-2023",
    "description": "Dernier modèle avec caméra haute résolution",
    "stock_quantity": 50,
    "category_id": 1
}

Base.metadata.create_all(engine)

inspector = inspect(engine)
tables = inspector.get_table_names()

if "category" in inspector.get_table_names():
    print("Table 'category' exists in PostgreSQL!")
    print(" Available tables:", tables)
else:
    print("Table 'category' does NOT exist in PostgreSQL.")

print("Tables created:", inspector.get_table_names())

# Check again after creation
inspector = inspect(engine)
tables = inspector.get_table_names()
print("Tables after creation:", tables)

def make_response(data, status_code=200):
    return jsonify(data), status_code

@app.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)  # Nécessite un refresh token valide
def refresh():
    try:
        current_user = get_jwt_identity()
        claims = get_jwt()
        
        # Récupérez l'utilisateur depuis la base de données si nécessaire
        db_session = Session()
        user = db_session.query(User).filter_by(email=current_user).first()
        
        new_access_token = create_access_token(
            identity=current_user,
            additional_claims={
                "user_id": claims.get('user_id'),
                "role": user.role  # Rechargez le rôle depuis la DB
            }
        )
        
        return jsonify({
            "access_token": new_access_token
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        db_session.close()
@app.route('/login', methods=['POST'])
def login():
    db_session = Session()
    try:
        controller = AuthController(db_session)
        return controller.login()
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        db_session.close()

@app.route('/')
def home():

    return "API E-Commerce en marche! Accédez à /products"

@app.route('/register', methods=['POST'])
def create_user():
    db_session = Session()
    controller = UserController(db_session)
    return controller.create_user()

@app.route('/register', methods=['GET'])
def get_all_users():
    db_session = Session()
    controller = UserController(db_session)
    return controller.get_all_users()

@app.route('/register/<int:user_id>', methods=['GET'])
def get_user_by_id(user_id):
    db_session = Session()
    controller = UserController(db_session)
    return controller.get_user_by_id(user_id)

@app.route('/register/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    db_session = Session()
    controller = UserController(db_session)
    return controller.update_user(user_id)

@app.route('/register/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    db_session = Session()
    controller = UserController(db_session)
    return controller.delete_user(user_id)

@app.route('/products', methods=['GET'])
@jwt_required()
def get_all_products():
    db_session=Session()
    
    try:
        products=db_session.query(Product).order_by(desc(Product.price)).all()
        products_data = [{
            'product_id': p.product_id,
            'name': p.name,
            'description': p.description,
            'price': p.price,
            'sku': p.sku,
            'stock_quantity': p.stock_quantity,
            'category_id': p.category_id
        } for p in products]
        return ApiResponse.success(
            message="Liste des produits récupérée avec succès",
            data=products_data,
            status_code=200
        )
    except Exception as e:
        return ApiResponse.error(
            message="Erreur lors de la récupération des produits",
            errors=str(e),
            status_code=500
        )
        
    finally:
        db_session.close()

@app.route('/products/<int:product_id>', methods=['GET'])
@jwt_required() 
def get_one_product(product_id):
    db_session = Session()
    try:
        product = db_session.query(Product).get(product_id)
        if not product:
            return ApiResponse.error(message="Produit non trouvé", status_code=404)

        # Convertir l'objet Product en dictionnaire
        product_data = {
            'product_id': product.product_id,
            'name': product.name,
            'description': product.description,
            'price': product.price,
            'sku': product.sku,
            'stock_quantity': product.stock_quantity,
            'category_id': product.category_id
        }

        return ApiResponse.success(
            message="Produit récupéré avec succès",
            data=product_data,
            status_code=200
        )
    except Exception as e:
        return ApiResponse.error(message=str(e), status_code=500)
    finally:
        db_session.close()

@app.route('/products', methods=['POST'])
@jwt_required() 
@admin_required
@toto
def create_product():
    db_session = Session()
    try:
        data = request.get_json()
        # Validation
        is_valid, error_msg = ProductValidator.validate_create(data)

        if not is_valid:
            return ApiResponse.error(message=error_msg, status_code=400)
        # Création
        product = ProductService(db_session).create_product(**data)

        return ApiResponse.success(
            message="Produit créé avec succès",
            data=product,
            status_code=201
        )

    except Exception as e:
        # Ne pas retourner e comme message si tu veux éviter les détails
        return ApiResponse.error(message="Une erreur est survenue", status_code=500)
    finally:
        db_session.close()

@app.route('/products/<int:product_id>', methods=['PUT'])
@jwt_required() 
@admin_required
def update_product(product_id):
    data=request.json
    session=Session()
    try:
        product=session.query(Product).get(product_id)

        if not product:
            return make_response({'error':'Product not found'},404)
        

        if 'name' in data:
            product.name=data['name']
        if 'price' in data:
            product.price=data['price']
        if 'description' in data:
            product.description=data['description']
        if 'sku' in data:
            product.sku=data['sku']
        if 'stock_quantity' in data:
            product.stock_quantity=data['stock_quantity']
        if 'category_id' in data:
            product.category_id=data['category_id']


        session.commit()
        return make_response({'message':'Product updated'})
    
    except Exception as e:
        session.rollback()
        return make_response({'error':str(e)},400)
    
    finally:
        session.close()        

@app.route('/products/<int:product_id>', methods=['DELETE'])
@jwt_required() 
@admin_required
def delete_product(product_id):
    session=Session()
    try:
        product=session.query(Product).get(product_id)
        if not product:
            return make_response({'error':'Product is not found'},404)

        session.delete(product)
        session.commit()
        return make_response({'message':'Product supprime'})
    
    except Exception as e:
        session.rollback()
        return make_response({'error':str(e)}, 400)
        
    finally:
        session.close()

@app.route('/products/categories/<int:category_id>', methods=['GET'])
@jwt_required() 
def get_products_by_category(category_id):
    db_session = Session()
    service = ProductService(db_session)
    try:
        products = service.get_products_by_category(category_id)
        result=[]
        for p in products:
              # On filtre bien sur category_id transmis en URL
             if p.category and p.category.category_id == category_id:
                result.append({
               'product_id': p.product_id,
                'name': p.name,
                'price': p.price,
                'category_id': p.category.category_id
            })
        return jsonify(result)
    finally:
        db_session.close()

from flask_jwt_extended import jwt_required

@app.route('/category', methods=['GET'])
@jwt_required()
def get_categories():
    db_session = Session()
    try:
        categories = db_session.query(Category).all()
        return ApiResponse.success(
            message="Liste des catégories récupérée",
            data=[{
                "category_id": cat.category_id,
                "name": cat.name,
                "description": cat.description
            } for cat in categories],
            status_code=200
        )
    except Exception as e:
        return ApiResponse.error(
            message="Erreur lors du traitement",
            errors=str(e),
            status_code=500
        )
    finally:
        db_session.close()

@app.route('/category', methods=['POST'])
@jwt_required()
@admin_required
def create_category():
    db_session = Session()
    try:
        data = request.get_json()

        if 'name' not in data:
            return ApiResponse.error(
                message="Le champ 'name' est obligatoire",
                status_code=400
            )
        
        category = Category(
            name=data['name'],
            description=data.get('description', '')
        )
        db_session.add(category)
        db_session.commit()
        
        return ApiResponse.success(
            message="Catégorie créée avec succès",
            data={
                "category_id": category.category_id,
                "name": category.name
            },
            status_code=201
        )
    except Exception as e:
        db_session.rollback()  
        return ApiResponse.error(
            message="Erreur lors du traitement",
            errors=str(e),
            status_code=500
        )
    finally:
        db_session.close()

@app.route('/category/<int:category_id>', methods=['PUT', 'DELETE'])
@jwt_required() 
@admin_required
def handle_single_category(category_id):
    db_session = Session()
    try:
        category = db_session.query(Category).get(category_id)
        if not category:
            return jsonify({"error": "Catégorie non trouvée"}), 404

        if request.method == 'PUT':
            data = request.get_json()
            
            # Validation des données
            if 'name' not in data:
                return jsonify({"error": "Le champ 'name' est obligatoire"}), 400
            
            # Mise à jour de la catégorie
            category.name = data['name']
            if 'description' in data:
                category.description = data['description']
            
            db_session.commit()
            
            return jsonify({
                "message": "Catégorie mise à jour avec succès",
                "category_id": category.category_id,
                "name": category.name,
                "description": category.description
            })

        elif request.method == 'DELETE':
            # Vérifier si la catégorie est utilisée par des produits
            product_count = db_session.query(Product).filter_by(category_id=category_id).count()
            if product_count > 0:
                return jsonify({
                    "error": "Impossible de supprimer cette catégorie",
                    "reason": f"{product_count} produit(s) y sont associés",
                    "solution": "Modifiez d'abord les produits ou supprimez-les"
                }), 400
            
            db_session.delete(category)
            db_session.commit()
            
            return jsonify({
                "message": "Catégorie supprimée avec succès",
                "deleted_category_id": category_id
            })

    except Exception as e:
        db_session.rollback()
        return jsonify({
            "error": str(e)
        }), 500
    finally:
        db_session.close()        
    
if __name__ == '__main__':
    app.run(debug=True)
