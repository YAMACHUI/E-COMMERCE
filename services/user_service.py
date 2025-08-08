from models.user import User
from sqlalchemy.orm import Session
from werkzeug.security import generate_password_hash, check_password_hash

class UserService:
    def __init__(self, db_session: Session):
        self.db = db_session

    def authenticate_user(self, email:str, password:str):
        user= self.db.query(User).filter_by(email=email).first()
        if not user:
            return None
        
        if not check_password_hash(user.password, password):
            return None
        
        return user
    
    def create_user(self, user_data):
        # Validate required fields exist
        required_fields = ['email', 'first_name', 'last_name', 'password', 'phone_number']
        for field in required_fields:
            if field not in user_data:
                raise ValueError(f"Missing required field: {field}")

        # Validation optionnelle du rôle
        if 'role' in user_data:
            if user_data['role'].lower() not in ['administrateur', 'utilisateur']:
                raise ValueError("Le rôle doit être 'administrateur' ou 'utilisateur'")

        existing_email = self.db.query(User).filter_by(email=user_data['email']).first()
        if existing_email:
            raise ValueError("Email already registered")
        
        existing_phone = self.db.query(User).filter_by(phone_number=user_data['phone_number']).first()
        if existing_phone:
            raise ValueError("Phone number already registered")  

        hashed_password = generate_password_hash(user_data['password'])

        # Création avec paramètres nommés
        new_user = User(
            email=user_data['email'],
            first_name=user_data['first_name'],
            last_name=user_data['last_name'],
            password=hashed_password,
            phone_number=user_data['phone_number'],
            role=user_data.get('role')  # .get() pour éviter KeyError
        )
        
        self.db.add(new_user)
        self.db.commit()
        self.db.refresh(new_user)
        return new_user

    def get_all_users(self):
        return self.db.query(User).order_by(User.user_id).all()

    def get_user_by_id(self, user_id: int):
        return self.db.query(User).filter_by(user_id=user_id).first()

    def update_user(self, user_id: int, update_data: dict):
        try:
            user = self.db.query(User).filter_by(user_id=user_id).first()
            if not user:
                return None

            allowed_fields = {'first_name', 'last_name', 'phone_number','role'}
            
            if 'phone_number' in update_data and update_data['phone_number']!= user.phone_number:
                existing_phone= self.db.query(User).filter(
                    User.phone_number==update_data['phone_number'],
                    User.user_id != user_id
                ).first()
                if existing_phone:
                    raise ValueError("Phone number already registered by another user")
                
            # Update only allowed fields
            for key, value in update_data.items():
                if key in allowed_fields:
                    if key == 'role':
                        # Conversion en minuscules et validation
                        value = value.lower()
                        if value not in ['administrateur', 'utilisateur']:
                            raise ValueError('Le rôle doit être "administrateur" ou "utilisateur"')
                    setattr(user, key, value)
            
            self.db.commit()  # Single commit after all updates
            self.db.refresh(user)
            
            return user
            
        except Exception as e:
            self.db.rollback()
            raise ValueError(f"Update failed: {str(e)}")

    def delete_user(self, user_id: int):
        user = self.get_user_by_id(user_id)
        if user:
            self.db.delete(user)
            self.db.commit()
        return user