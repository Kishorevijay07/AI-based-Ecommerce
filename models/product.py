# models/product.py
from pydantic import BaseModel, Field
from typing import Optional, List, Dict


class ProductBase(BaseModel):
    title: str
    description: Optional[str] = None

    # Keep raw scraped price + parsed float
    raw_price: Optional[str] = None
    price: Optional[float] = None
    currency: Optional[str] = None

    rating: Optional[float] = None
    review_count: Optional[int] = None
    reviews: List[Dict] = Field(default_factory=list)

    about_heading: Optional[str] = None
    about_items: List[str] = Field(default_factory=list)

    images: List[str] = Field(default_factory=list)
    main_image: Optional[str] = None

    product_details: Dict[str, str] = Field(default_factory=dict)
    related_links: List[str] = Field(default_factory=list)

    category: Optional[str] = None
    stock: Optional[int] = None


class ProductCreate(ProductBase):
    """Use this for POST /products (client -> server)"""
    pass


class ProductResponse(ProductBase):
    """
    Use this for API responses to the client.
    We return `id` as a string (converted from MongoDB _id).
    created_at/updated_at are ISO strings to keep serialization simple.
    """
    id: str
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
