
from flask import request, jsonify
from services.user_service import UserService
from Validator.user_validator import validate_user_creation_data, validate_user_update_data

class UserController:
    def __init__(self, db_session):
        self.user_service = UserService(db_session)

    def create_user(self):
        try:
            data = request.get_json()
            validate_user_creation_data(data) 
            user = self.user_service.create_user(data)
            return jsonify({"message": "Utilisateur créé avec succès", "user": user.to_dict()}), 201
        
        except Exception as e:
            return jsonify({"error": str(e)}), 409

    def get_all_users(self):
        try:
            users = self.user_service.get_all_users()
            return jsonify([user.to_dict() for user in users]), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    def get_user_by_id(self, user_id):
        try:
            user = self.user_service.get_user_by_id(user_id)
            if user:
                return jsonify(user.to_dict()), 200
            else:
                return jsonify({"error": "Utilisateur non trouvé"}), 404
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    def update_user(self, user_id):
        try:
            data = request.get_json()
            validate_user_update_data(data)
            update_data = {
            'first_name': data.get('first_name'),
            'last_name': data.get('last_name'),
            'phone_number': data.get('phone_number'),
            'role':data.get('role')
        }
             # Suppression des valeurs None
            update_data = {k: v for k, v in update_data.items() if v is not None}

            if not update_data:
                    return jsonify({"error": "Aucune donnée valide à mettre à jour"}), 400
            
            updated_user = self.user_service.update_user(
            user_id=user_id,
            update_data=update_data
        )
            if updated_user:
                return jsonify({"message": "Utilisateur mis à jour avec succès", "user": updated_user.to_dict()}), 200
            else:
                return jsonify({"error": "Utilisateur non trouvé"}), 404
        except Exception as e:
            return jsonify({"error": str(e)}), 400

    def delete_user(self, user_id):
        try:
            success = self.user_service.delete_user(user_id)
            if success:
                return jsonify({"message": "Utilisateur supprimé avec succès"}), 200
            else:
                return jsonify({"error": "Utilisateur non trouvé"}), 404
        except Exception as e:
            return jsonify({"error": str(e)}), 500