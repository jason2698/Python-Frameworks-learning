from fastapi import FastAPI
from model import Product

app = FastAPI()

@app.get('/')
def greet():
    return 'Hello from Python Learning'

products = [
    Product(id=1,name='IPhone', description='16 pro max', price=149000, quantity=50)
]
@app.get('/products')
def getProducts():
    return products

@app.get('/product/{id}')
def get_product_id(id:int):
    for product in products:
        if product.id == id:
            return product
    return 'Product Not Found'

@app.post('/product')
def add_product(product:Product):
    products.append(product)
    return product