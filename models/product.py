from sqlalchemy import Column, Integer, String, Float, Text, ForeignKey
from sqlalchemy.orm import relationship
from models.base import Base

class Product(Base):
    __tablename__ = 'products'

    product_id = Column(Integer, primary_key=True)
    name = Column(String(100), unique=True, nullable=False)
    description = Column(Text)
    sku = Column(String(50), unique=True)
    price = Column(Float, nullable=False)
    stock_quantity = Column(Integer, default=0)
    
    # Define the foreign key and relationship to Category
    category_id = Column(Integer, ForeignKey('category.category_id', name='fk_product_category'))
    category = relationship("Category", back_populates="products")

    def to_dict(self):
     return {
        "product_id": self.product_id,
        "name": self.name,
        "price": self.price,
        "sku": self.sku,
        "description": self.description,
        "stock_quantity": self.stock_quantity,
        "category_id": self.category_id,
    }


    def __repr__(self):
        return f"<Product(name='{self.name}', price={self.price})>"
