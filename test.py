from sqlalchemy import create_engine,inspect
from sqlalchemy.orm import sessionmaker
from models.product import Base,Product
from models.category import Category

db_user="postgres"
db_password="YAMACHUI"
db_host="localhost"
db_port="2006"
db_name="e-commerce"


db_url= "postgresql+psycopg2://postgres:YAMACHUI@localhost:2006/e-commerce"
engine = create_engine(db_url,echo=True)

try:
    
 # Création des tables
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    inspector=inspect(engine)
    print("Tables crées:", inspector.get_table_names)

    Session=sessionmaker(bind=engine)
    session=Session()

    # Création d'une catégorie
    chaussures_cat = Category(
        name='Chaussures',
        description="Catégorie pour toutes les chaussures"
    )
    session.add(chaussures_cat)
    session.commit()

    # Création d'un produit
    chaussure = Product(
        name='chaussure',
        description="Une belle paire de chaussure",
        price=20.000,  # Changé en float
        sku="chaussure-Nike-Blanc",
        stock_quantity=50,  # Changé en int
        category_id=chaussures_cat.id  # Ajouté la relation
    )
    
    session.add(chaussure)
    session.commit()

    print("Produit inséré avec succès !")


except Exception as ex:
 print("connection failed:",ex)
 session.rollback()
finally:
    session.close()
