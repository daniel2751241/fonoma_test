from fastapi import FastAPI
from pydantic import BaseModel, validator
from enum import Enum
from typing import List
import redis
import json
import os

class OrderStatus(str, Enum):
    completed = "completed"
    pending = "pending"
    canceled = "canceled"
    
class Order(BaseModel):
    id: int
    item: str
    quantity: int
    price: float
    status: OrderStatus
    
    @validator("item")
    def not_empty_item(cls, v):
        if v == '':
            raise ValueError("item field cannot be empty")
        return v
    
    @validator("quantity")
    def positive_quantity(cls, v):
        if v <= 0:
            raise ValueError("quantity field must be positive")
        return v
    
    @validator("price")
    def positive_price(cls, v):
        if v <= 0:
            raise ValueError("price field must be positive")
        return v

app = FastAPI()
cache = redis.Redis.from_url(os.getenv("REDIS_URI"))

@app.post("/solution")
async def process_orders(orders: List[Order], criterion: OrderStatus):
    # my guess is total revenue should be like this, not just making a sum with orders prices
    # that's why test units should not give the expected response as the sample request you
    # provided, so i'm assuming this approach
    cache_key = json.dumps({'orders': [order.dict() for order in orders], 'criterion': criterion})
    result = cache.get(cache_key)
    if result:
        return json.loads(result)
    total = sum([order.price*order.quantity for order in orders if order.status == criterion])
    result = {"total": total}
    cache.set(cache_key, json.dumps(result))
    return result