from uuid import UUID
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class User(BaseModel):
    id: Optional[UUID]
    first_name: str
    email: str
    last_name: str

class Food(BaseModel):
    id: Optional[UUID]
    name: str
    description: str
    price: float
    image_url: Optional[str]

class Cart(BaseModel):
    id: Optional[UUID]
    user_id: UUID
    food_items: List[UUID]  

class Checkout(BaseModel):
    id: Optional[UUID]
    user_id: UUID
    cart_id: UUID
    total_price: float
    date: datetime

class Delivery(BaseModel):
    id: Optional[UUID]
    checkout_id: UUID
    address: str
    delivery_date: datetime
    status: str
