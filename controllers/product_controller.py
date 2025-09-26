from datetime import datetime
from typing import List, Optional
from bson import ObjectId
from fastapi import HTTPException

from config import db
from models.product import ProductCreate, ProductResponse


def _transform_doc(doc: dict) -> dict:
    """
    Convert MongoDB document to a dict suitable for ProductResponse:
      - turn _id -> id (string)
      - convert datetimes to ISO strings
    """
    d = dict(doc)  # copy
    _id = d.get("_id")
    d["id"] = str(_id) if _id is not None else None
    d.pop("_id", None)

    # normalize created_at / updated_at to ISO strings (if present)
    for k in ("created_at", "updated_at"):
        if k in d and d[k] is not None:
            try:
                d[k] = d[k].isoformat()
            except Exception:
                d[k] = str(d[k])
    return d


async def create_product(payload: ProductCreate) -> ProductResponse:
    doc = payload.model_dump(exclude_none=True)
    now = datetime.utcnow()
    doc["created_at"] = now
    doc["updated_at"] = now

    result = await db["products"].insert_one(doc)
    if not result.inserted_id:
        raise HTTPException(status_code=500, detail="Failed to insert product")

    inserted = await db["products"].find_one({"_id": result.inserted_id})
    if not inserted:
        raise HTTPException(status_code=500, detail="Inserted product not found")

    transformed = _transform_doc(inserted)
    return ProductResponse(**transformed)


async def get_products() -> List[ProductResponse]:
    products: List[ProductResponse] = []
    cursor = db["products"].find().sort("created_at", -1)
    async for doc in cursor:
        transformed = _transform_doc(doc)
        products.append(ProductResponse(**transformed))
    return products




async def get_product(product_id: str) -> ProductResponse:
    if not ObjectId.is_valid(product_id):
        raise HTTPException(status_code=400, detail="Invalidddddd product ID")

    doc = await db["products"].find_one({"_id": ObjectId(product_id)})
    if not doc:
        raise HTTPException(status_code=404, detail="Product not found")

    transformed = _transform_doc(doc)
    return ProductResponse(**transformed)
