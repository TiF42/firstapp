# app.py
import streamlit as st
import requests
from fastapi import FastAPI
from pydantic import BaseModel
import threading

# ----------------- FASTAPI SETUP -----------------
api = FastAPI()

# Simple in-memory database
items = {}

class Item(BaseModel):
    name: str
    price: float

@api.get("/")
def root():
    return {"message": "FastAPI is running!"}

@api.get("/items/{item_id}")
def get_item(item_id: int):
    return items.get(item_id, {"error": "Item not found"})

@api.post("/items/{item_id}")
def create_item(item_id: int, item: Item):
    items[item_id] = {"name": item.name, "price": item.price}
    return {"message": f"Item {item_id} added!", "item": items[item_id]}

# Function to run FastAPI in background thread
def run_api():
    import uvicorn
    uvicorn.run(api, host="127.0.0.1", port=8000)

# Run FastAPI in a background thread
threading.Thread(target=run_api, daemon=True).start()

# ----------------- STREAMLIT FRONTEND -----------------
st.title("Easy FastAPI + Streamlit Demo")

api_url = "http://127.0.0.1:8000/items"

# Add item
st.header("Add an Item")
item_id = st.number_input("Item ID", min_value=1, step=1)
name = st.text_input("Name")
price = st.number_input("Price", min_value=0.0, step=0.01)

if st.button("Add Item"):
    data = {"name": name, "price": price}
    response = requests.post(f"{api_url}/{item_id}", json=data)
    st.write(response.json())

# Get item
st.header("Get an Item")
get_id = st.number_input("Item ID to fetch", min_value=1, step=1, key="get")
if st.button("Fetch Item"):
    response = requests.get(f"{api_url}/{get_id}")
    st.write(response.json())