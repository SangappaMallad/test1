from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

# Dummy database
products = []

class Product(BaseModel):
    id: int
    name: str
    price: float


@app.get("/")
def health_check():
    return {"message": "API is running on local server"}


# Get all products
@app.get("/products")
def get_products():
    return products


# Add product
@app.post("/products")
def add_product(product: Product):
    products.append(product.dict())
    return {
        "message": "Product added successfully",
        "product": product
    }


# Delete product by id
@app.delete("/products/{product_id}")
def delete_product(product_id: int):

    for product in products:
        if product["id"] == product_id:
            products.remove(product)
            return {"message": "Product deleted successfully"}

    raise HTTPException(
        status_code=404,
        detail="Product not found"
    )