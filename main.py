from fastapi import FastAPI, Depends
from model import Product
from database import session, engine
import database_models
from sqlalchemy.orm import Session

app = FastAPI()

database_models.Base.metadata.create_all(bind=engine)

@app.get('/')
def greet():
    return 'Hello from Python Learning'

products = [
    Product(id=1,name='IPhone', description='16 pro max', price=149000, quantity=50)
]

def get_db():
    db = session()
    try:
        yield db
    finally:
        db.close()

def init_db():
    db = session() #where ever we want database connection, we have to use this line
    
    count = db.query(database_models.Product).count
    if count == 0:
        for product in products:
            db.add(database_models.Product(**product.model_dump()))  #model_dump - Give you a dictonary, ** - unpacking
            
        db.commit()        
init_db()

@app.get('/products')
def getProducts(db: Session = Depends(get_db)):
    db_products = db.query(database_models.Product).all()
    
    return db_products

@app.get('/product/{id}') 
def get_product_id(id:int, db: Session = Depends(get_db)):
    db_product = db.query(database_models.Product).filter(database_models.Product.id == id).first()
    if db_product:
        return db_product
    return 'Product Not Found'

@app.post('/product')
def add_product(product:Product):
    products.append(product)
    return product

@app.put('/product')
def update_product(id:int, product:Product):
    for i in range(len(products)):
        if products[i].id == id:
            products[i] = product
            return "Product Updated Successfully"

    return "No Product Found"

@app.delete('/product')
def delete_product(id:int):
    for i in range(len(products)):
        if products[i].id == id:
            del products[i]
            return 'Product deleted Successfully'
    
    return 'No Product Found'