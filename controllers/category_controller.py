import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from flask import request, jsonify
from services.category_service import CategoryService

class CategoryController:
    @staticmethod
    def create_category(db_session):
        try:
            data = request.get_json()
            if not data.get('name') or not data.get('description'):
                return jsonify({"error": "Missing required fields"}), 400
            
            service = CategoryService(db_session)
            new_category = service.create_category(
                name=data['name'],
                description=data.get('description')
            )
            return jsonify({
                "message": "Category created",
                "id": new_category.category.id
            }), 201
        except Exception as e:
            return jsonify({"error": str(e)}), 400



    @staticmethod
    def get_all_categories(service: CategoryService):
        categories = service.get_all_categories()
        return jsonify([{
            'id': c.category_id,
            'name': c.name,
            'description': c.description
        } for c in categories])
