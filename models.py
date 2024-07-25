from sqlalchemy import Column, Integer, Float
from database import Base

class ProductDB(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    price = Column(Float, nullable=False)
