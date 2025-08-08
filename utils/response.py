from flask import jsonify

class ApiResponse:
    @staticmethod
    def success(data=None, message="Succès", status_code=200):
         return jsonify({
            "status": "success",
            "message": message,
             "data": data
            
        }), status_code
    
    @staticmethod
    def error(message="Erreur", status_code=500):
           return jsonify({
            "status": "error",
            "message": message,
            "data": None
        }), status_code