from flask import request, jsonify
from werkzeug.security import check_password_hash
from services.user_service import UserService
from models.user import User
from flask_jwt_extended import create_access_token, create_refresh_token
from datetime import timedelta

class AuthController:
    def __init__(self, db_session):
        self.user_service= UserService(db_session)


    def login(self):
        try:
            data=request.get_json()
            email=data.get('email')
            password=data.get('password')

            if not email or not password:
                return jsonify({"error": "Email et mot de passe requis"}), 400
            
            # Utilisation cohérente de user_service
            user = self.user_service.authenticate_user(email, password)
            
            if not user:
                return jsonify({"error": "Email ou mot de passe incorrect"}), 401
            
            # Création du token JWT avec les information 
            access_token=create_access_token(
                identity=user.email,
                additional_claims={
                    "user_id": user.user_id,
                    "role": user.role
                },
            )

            refresh_token = create_refresh_token(
                identity=user.email,
                additional_claims={
                    "user_id": user.user_id
                }
            )

            return jsonify({
            "message": "Connexion réussie",
            "access_token":access_token,
            "refresh_token": refresh_token,
            "user": {
                "user_id": user.user_id,
                "email": user.email,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "role":user.role
            }
        }), 200
        
        except Exception as e:
            return jsonify({"error":str(e)}),500