from models.category import Category
from sqlalchemy.orm import Session

class CategoryService:
    def __init__(self, db_session):
        self.db_session = db_session

    def create_category(self, name, description):
        try:
            # Create a new category
            new_category = Category(name=name, description=description)
            
            # Add the new category to the session and commit
            self.db_session.add(new_category)
            self.db_session.commit()
            
            return new_category
        except Exception as e:
            # Handle any errors that might occur
            self.db_session.rollback()
            raise Exception("Failed to create category: " + str(e))
