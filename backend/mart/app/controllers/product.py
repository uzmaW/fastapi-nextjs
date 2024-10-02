import os
import shutil
import uuid
from fastapi import Form, Query, UploadFile, File, Depends
from fastapi.responses import JSONResponse
from fastapi import APIRouter
from sqlalchemy import select
from ..db.models.product import Product
from ..db.models.product import ProductImages
from ..db.models.product import ProductVariants
from typing import List
from ..db.conn import get_db

from sqlmodel import Session

class ProductController:
    def __init__(self):
        self.router = APIRouter(prefix="/products", tags=["products"])
        self.router.add_api_route("/", self.get_products, methods=["GET"])
        self.router.add_api_route("/create", self.create_product, methods=["POST"])
        self.router.add_api_route("/get/{product_id}", self.get_product, methods=["GET"])
        self.router.add_api_route("/update/{product_id}", self.update_product, methods=["PUT"])
        self.router.add_api_route("/delete/{product_id}", self.delete_product, methods=["DELETE"])

    @staticmethod
    async def get_products(self,  offset: int = 0, limit: int = Query(default=100, le=100),  db:Session=Depends(get_db)):
        products = db.exec(select(Product).offset(offset).limit(limit)).all()
        return products

    @staticmethod
    async def create_product(
        name: str = Form(...),
    price: float = Form(...),
    description: str = Form(...),
    images: List[UploadFile] = File(...),
        db: Session = Depends(get_db)
    ):
        try:
            # 1. Handle image uploads and store them (e.g., on cloud storage or local filesystem)
            # Handle image uploads
            image_urls = []
            for image in images:
                # Generate a unique filename
                filename = f"{uuid.uuid4()}.{image.filename.split('.')[-1]}"
            
            # Define the path where the image will be saved
            file_path = f"static/product_images/{filename}"
            
            # Ensure the directory exists
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            
            # Save the file
            with open(file_path, "wb") as buffer:
                shutil.copyfileobj(image.file, buffer)
            
            # Generate the URL for the saved image
            image_url = f"/static/product_images/{filename}"
            image_urls.append(image_url)
      

           # 2. Create the product in your database
            new_product = Product(name=name, price=price, description=description, image_urls=image_urls)
            db.add(new_product)
            db.commit()
            db.refresh(new_product)

            # 3. Create the product images in your database
            for image_url in image_urls:
                new_image = ProductImages(image_url=image_url, product_id=new_product.id)
                db.add(new_image)
            db.commit()

            return JSONResponse(content={"message": "Product created successfully", "product_id": new_product.id}, status_code=201)
        except Exception as e:
        # Handle exceptions and return an error response
            print(f"Error creating product: {e}")
            return JSONResponse(content={"error": "Failed to create product"}, status_code=500)

    async def get_product(self, product_id: int, db: Session = Depends(get_db)):
        product = db.exec(select(Product).where(Product.id == product_id)).first()
        if not product:
            return JSONResponse(content={"error": "Product not found"}, status_code=404)
        return product

    async def update_product(self, product_id: int, name: str = Form(...), price: float = Form(...), description: str = Form(...), images: List[UploadFile] = File(...), db: Session = Depends(get_db)):
        product = db.exec(select(Product).where(Product.id == product_id)).first()
        if not product:
            return JSONResponse(content={"error": "Product not found"}, status_code=404)

        product.name = name
        product.price = price
        product.description = description
        
        db.add(product)
        db.commit()
        db.refresh(product)

        return JSONResponse(content={"message": "Product updated successfully", "product_id": product.id}, status_code=200)

    async def delete_product(self, product_id: int, db: Session = Depends(get_db)):
        product = db.exec(select(Product).where(Product.id == product_id)).first()
        if not product:
            return JSONResponse(content={"error": "Product not found"}, status_code=404)

        db.delete(product)
        db.commit()

        return JSONResponse(content={"message": "Product deleted successfully", "product_id": product.id}, status_code=200)
    
