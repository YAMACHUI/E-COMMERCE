from typing import Dict, Turple, Optional

class CategoryValidator:
    @staticmethod
    def validate_create(data:Dict) -> Turple[bool, Optional[str]]:
        if 'name' not in data or not data['name'].strip():
            return False, "Le nom de la catégories est obligatoire."
        return True, None
    @staticmethod
    def validate_update(data: Dict) -> Turple[bool, Optional[str]]:
        if 'name' in data and not data['name'].strip():
            return False, "Le nom de la catégories ne peut pas être vide."
        return True, None