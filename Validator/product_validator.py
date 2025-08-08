from flask import request
from typing import Dict, Optional,Tuple

class ProductValidator:
    @staticmethod
    def validate_create(data: Dict) -> Tuple[bool, Optional[str]]:
        """Valide les données pour la creation d'un produit"""
        required_fields=['name','price', 'sku', 'category_id']
        for field in required_fields:
            if field not in data:
                return False, f"Le champ '{field}' est obligatoire."
            
        #Validation du prix
        if not isinstance(data['price'], (int, float)) or data['price'] <=0:
            return False, "Le prix doit être un nombre positif."
        
        #validation de category_id
        if not isinstance(data['category_id'],int) or data['category_id'] <=0:
            return False, "L'ID de la catégorie doit être un entier positif."
        
        #validation du nom
        if len(data['name'])<2 or len(data['name']) >100:
            return False, "Le nom doit contenir entre 2 et 100 caractères"
        
        #Validation du sku
        if len(data['sku']) <3 or len(data['sku'])>50:
            return False, "Le SKU doit contenir entre 3 et 50 caractères"
        
        return True, None

    @staticmethod
    def validate_update(data: Dict)  -> Tuple[bool, Optional[str]]:
        """Valide les données pour la mise à jour d'un produit."""
        if 'price' in data and (not isinstance(data['price'], (int, float)) or data['price'] <= 0):
            return False, "Le prix doit être un nombre positif."
        return True, None  
            
