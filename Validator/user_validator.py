
import re

def validate_user_creation_data(data):
    """Validation pour la création d'utilisateur"""
    required_fields = ['first_name', 'last_name', 'email', 'phone_number', 'password','role']
    
    for field in required_fields:
        if field not in data or not str(data[field]).strip():
            raise ValueError(f"Le champ '{field}' est requis.")
    
    if 'role' in data:
        if data['role'].lower() not in ['administrateur', 'utilisateur']:
            raise ValueError('Le role doit être "administrateur" ou "utilisateur"')
    
    validate_email_format(data['email'])
    validate_phone_number(data['phone_number'])
    validate_password(data.get('password',''))

def validate_user_update_data(data):
    """Validation pour la mise à jour d'utilisateur"""
    if not data:
        raise ValueError("Aucune donnée fournie")

    allowed_fields = {'first_name', 'last_name', 'phone_number','role'}
    
    # Vérifie qu'au moins un champ modifiable est présent
    if not any(field in data and str(data[field]).strip() for field in allowed_fields):
        raise ValueError("Au moins un champ modifiable doit être fourni")

    if 'email' in data:
        raise ValueError("La modification d'email n'est pas autorisée")
    
    if 'password' in data:
        raise ValueError("Utilisez la route dédiée pour modifier le mot de passe")

    if 'phone_number' in data:
        validate_phone_number(data['phone_number'])

    if 'role' in data:
        if data['role'].lower() not in ['administrateur', 'utilisateur']:
            raise ValueError('Le rôle doit être "administrateur" ou "utilisateur"')    

def validate_email_format(email):
    if not re.match(r'^[a-zA-Z0-9._%+-]+@gmail\.com$', email):
        raise ValueError("L'email doit se terminer par @gmail.com")

def validate_phone_number(phone_number):
    if not re.match(r"^\+?[0-9]{9,15}$", str(phone_number)):
        raise ValueError("Numéro de téléphone invalide.")

def validate_password(password):
    if not password:
        raise ValueError("Le mot de passe ne peut pas être vide")
    if len(password) > 8:
        raise ValueError("Le mot de passe doit contenir au moins 8 caractères.")