from database import Base, engine
from models import ProductDB

# Create the database tables
Base.metadata.create_all(bind=engine)
