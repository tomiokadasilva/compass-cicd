from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List

from database import get_db
from models import ProductDB

app = FastAPI()

class Product(BaseModel):
    id: int
    price: float

class PriceUpdate(BaseModel):
    id: int
    price: float

@app.post("/register-product/") #curl -X POST "http://127.0.0.1:8000/register-product" -H "Content-Type: application/json" -d '{"id": 1, "price": 19.99}'
def register_product(product: Product, db: Session = Depends(get_db)):
    db_product = db.query(ProductDB).filter(ProductDB.id == product.id).first()
    if db_product:
        raise HTTPException(status_code=400, detail="Product ID already exists")
    db_product = ProductDB(id=product.id, price=product.price)
    db.add(db_product)
    db.commit()
    return {"message": "Product registered successfully", "product": {"id": db_product.id, "price": db_product.price}}

@app.patch("/change_price/") #curl -X PATCH "http://127.0.0.1:8000/change_price/" -H "Content-Type: application/json" -d '{"product_id": 1, "price": 49.99}'
def change_price(update: PriceUpdate, db: Session = Depends(get_db)):
    db_product = db.query(ProductDB).filter(ProductDB.id == update.id).first()
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")
    db_product.price = update.price
    db.commit()
    return {"message": "Product price updated successfully", "product": {"id": db_product.id, "price": db_product.price}}

@app.get("/product/{product_id}") #curl -X GET "http://127.0.0.1:8000/product/1"
def get_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(ProductDB).filter(ProductDB.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return {"product": {"id": product.id, "price": product.price}}

@app.get("/products") #curl -X GET "http://127.0.0.1:8000/products"
def list_products(db: Session = Depends(get_db)):
    products = db.query(ProductDB).all()
    return {"products": [{"id": product.id, "price": product.price} for product in products]}

@app.delete("/delete_product/{product_id}") #curl -X DELETE "http://127.0.0.1:8000/delete_product/1"
def delete_product(product_id: int, db: Session = Depends(get_db)):
    db_product = db.query(ProductDB).filter(ProductDB.id == product_id).first()
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")
    db.delete(db_product)
    db.commit()
    return {"message": "Product deleted successfully"}
