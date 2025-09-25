from pydantic import BaseModel, Field
from typing import Optional

class User(BaseModel):
    id: Optional[str] = Field(default=None, alias="_id")
    name: str
    email: str
    password: str
    phone_number: int

    class Config:
        extra = "ignore"
