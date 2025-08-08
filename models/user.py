from sqlalchemy import Column, Integer, String
from models.base import Base

class User(Base):
    __tablename__ = 'users'

    user_id = Column(Integer, primary_key=True)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    phone_number = Column(String(15))
    password = Column(String(200), nullable=False)
    role=Column(String(20), nullable=False, default='utilisateur')

    def __init__(self, email, first_name, last_name, password, phone_number, **kwargs):
            self.email = email
            self.first_name = first_name
            self.last_name = last_name
            self.password = password
            self.phone_number = phone_number
            self.role = kwargs.get('role', 'utilisateur').lower()

    def to_dict(self):
        return {
            "user_id": self.user_id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "phone_number": self.phone_number,
            "role":self.role
        }