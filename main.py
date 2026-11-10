from fastapi import FastAPI, Depends, File, UploadFile, HTTPException
from model import Product
from database import session, engine
import database_models
from sqlalchemy.orm import Session
from pathlib import Path
from routes.employees import router as employees_router
from config import settings

app = FastAPI(
    title=settings.app_name,
    debug=settings.debug
)

app.include_router(employees_router)

database_models.Base.metadata.create_all(bind=engine)

@app.get('/')
def greet():
    return {
        'message' : 'Hello from Python Learning',
        'application' : settings.app_name,
        'environment' : settings.environment
    }

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
def add_product(product:Product, db : Session = Depends(get_db)):
    db.add(database_models.Product(**product.model_dump()))
    db.commit()
    return product

@app.put('/product')
def update_product(id:int, product:Product, db:Session = Depends(get_db)):
    db_product = db.query(database_models.Product).filter(database_models.Product.id == id).first()
    if not db_product:
        return "No Product Found"
    
    db_product.name = product.name
    db_product.price = product.price
    db_product.description = product.description
    db_product.quantity = product.quantity
    db.commit()
    # db.refresh(db_product)
    
    return "Product Updated Successfully"

@app.delete('/product')
def delete_product(id:int):
    for i in range(len(products)):
        if products[i].id == id:
            del products[i]
            return 'Product deleted Successfully'
    
    return 'No Product Found'

# File Upload Related Code
UPLOAD_DIR = Path('uploads')
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

ALLOWED_EXT = {'.pdf', '.png', '.jpg', '.jpeg'}

@app.post('/upload')
async def upload_file(file:UploadFile = File(...)):
    extension = Path(file.filename or '').suffix.lower()

    if extension not in ALLOWED_EXT:
        raise HTTPException(
            status_code= 400,
            detail='Only PDF and Image files are allowed'
        )
    
    destination = UPLOAD_DIR / f"uploaded_file{extension}"

    try:
        with destination.open('wb') as output:
            while chunk := await file.read(1024 * 1024):
                output.write(chunk)
    finally:
        await file.close()

    return {
        "message" : "File Uploaded Successfully",
        "filename" : destination.name
    }