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


# from services.Scrappers import search_via_internet
# import asyncio


# @router.get('/search-via-internet', response_model=dict)
# async def search_via_internet_route():
#     url = "https://www.amazon.in/dp/B0FDL3VZR8"
#     result = await search_via_internet(url)
#     return result

