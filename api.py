from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()
items = {}  # In-memory storage

class Item(BaseModel):
    name: str
    price: float

@app.get("/")
def read_root():
    return {"message": "Hello! FastAPI is running."}

@app.get("/items/{item_id}")
def get_item(item_id: int):
    return items.get(item_id, {"error": "Item not found."})

@app.post("/items/{item_id}")
def create_item(item_id: int, item: Item):
    items[item_id] = item
    return {"message": f"Item {item_id} created", "item": item}