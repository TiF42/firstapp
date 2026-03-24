import streamlit as st
import requests

st.set_page_config(page_title="Streamlit + FastAPI Demo", page_icon="💻", layout="centered")
st.title("💻 Streamlit + FastAPI Demo")

st.write("This demo lets you add items to an API and fetch them easily.")

API_URL = "http://127.0.0.1:8000/items"

# --- Section: Add Item ---
st.header("1️⃣ Add a New Item")
st.write("Fill in the details and click 'Add Item'.")

item_id = st.number_input("Item ID", min_value=1, step=1, value=1)
name = st.text_input("Item Name", value="Sample Item")
price = st.number_input("Item Price", min_value=0.0, step=0.01, value=9.99)

if st.button("Add Item"):
    data = {"name": name, "price": price}
    response = requests.post(f"{API_URL}/{item_id}", json=data)
    st.success(response.json())

# --- Section: Fetch Item ---
st.header("2️⃣ Fetch an Existing Item")
st.write("Enter the ID of an item and click 'Fetch Item'.")

fetch_id = st.number_input("Item ID to fetch", min_value=1, step=1, value=1, key="fetch")
if st.button("Fetch Item", key="fetch_btn"):
    response = requests.get(f"{API_URL}/{fetch_id}")
    st.info(response.json())