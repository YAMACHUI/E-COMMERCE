import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from sqlalchemy import create_engine, asc, desc
from sqlalchemy.orm import sessionmaker, Session
from models.product import Product,Base

class ProductService:
    def __init__(self, db_session: Session):
        self.db = db_session

    def get_all_products_by_price_desc(self):
        try:
            return self.db.query(Product).order_by(Product.price.desc()).all()
        except Exception as e:
            self.db.rollback()
            raise ValueError(f"Erreur de récupération des produits : {str(e)}")

    def create_product(self, name: str, price: float, description: str, sku: str,category_id:int,stock_quantity: int = 0):
        """Crée un nouveau produit avec validation"""
        if price <= 0:
            raise ValueError("Le prix doit être positif")
        if stock_quantity < 0:
            raise ValueError("Le stock ne peut pas être négatif")
        if not sku or len(sku) < 4:
            raise ValueError("Le SKU est trop court")
        if not name or len(name) < 3:
            raise ValueError("Le nom est trop court")

        existing = self.db.query(Product).filter((Product.name == name) | (Product.sku == sku)).first()
        if existing:
            raise ValueError("Un produit avec ce nom ou SKU existe déjà")

        product = Product(
            name=name,
            price=price,
            sku=sku,
            description=description,
            stock_quantity=stock_quantity,
            category_id=category_id
        )
        self.db.add(product)
        self.db.commit()
        self.db.refresh(product)
        return product.to_dict()

    def get_products_by_category(self, category_id: int):
        """Get all products belonging to a specific category triés par product_id"""
        return (
            self.db.query(Product)
            .filter(Product.category_id == category_id)
            .order_by(asc(Product.product_id))
            .all()
        )


# --------- TEST DE LA CLASSE ----------
if __name__ == "__main__":
    # Connexion à la base PostgreSQL
    DATABASE_URL = "postgresql+psycopg2://postgres:YAMACHUI@localhost:2006/e-commerce"
    engine = create_engine(DATABASE_URL, echo=False)
    SessionLocal = sessionmaker(bind=engine)
    session = SessionLocal()

    # Création des tables (si jamais)
    Base.metadata.create_all(bind=engine)

    service = ProductService(db_session=session)

    try:
        print("Tentative de création du produit...")
        product = service.create_product(
            name="TestProduit",
            price=50.0,
            sku="SKU1234",
            description="Produit de test",
            stock_quantity=10,
            category_id=1,
        )
        print(" Produit créé :", product)

    except Exception as e:
        print(" Erreur :", e)
