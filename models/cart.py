from .base import Base
from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship

class Cart(Base):
    __tablename__ = 'carts'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.user_id'))
    items = relationship('CartItem', back_populates='cart')

class CartItem(Base):
    __tablename__ = 'cart_items'
    
    id = Column(Integer, primary_key=True)
    cart_id = Column(Integer, ForeignKey('carts.id'))
    product_id = Column(Integer, ForeignKey('products.product_id'))
    stock_quantity = Column(Integer, default=1)
    
    cart = relationship('Cart', back_populates='items')
    product = relationship('Product')