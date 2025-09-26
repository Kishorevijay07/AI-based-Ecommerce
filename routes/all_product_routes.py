from services.Scrappers import search_via_internet
import asyncio
from fastapi import APIRouter
from typing import List


router = APIRouter(prefix="/all_products", tags=["All_Products"])

@router.get('/search-via-internet', response_model=dict)
async def search_via_internet_route():
    url = "https://www.amazon.in/dp/B0FDL3VZR8"
    result = await search_via_internet(url)
    return result

