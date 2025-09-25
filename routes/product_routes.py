from fastapi import APIRouter
from typing import List

from models.product import ProductCreate, ProductResponse
from controllers import product_controller

router = APIRouter(prefix="/products", tags=["Products"])


@router.post("/", response_model=ProductResponse)
async def create_product_route(payload: ProductCreate):
    return await product_controller.create_product(payload)


@router.get("/", response_model=List[ProductResponse])
async def get_products_route():
    return await product_controller.get_products()


@router.get("/{product_id}", response_model=ProductResponse)
async def get_product_route(product_id: str):
    return await product_controller.get_product(product_id)



from services.Scrappers import web_scraper_service
@router.get('/search-via-internet')
async def search_via_internet_route(url: str):
    print("url", url)

    return await product_controller.web_scraper_service(url)