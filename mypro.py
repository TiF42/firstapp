import streamlit as st
import requests

st.title("Streamlit + FastAPI Demo")

api_url = "http://127.0.0.1:8000/items"

# Create item
st.header("Add Item")
item_id = st.number_input("Item ID", min_value=1, step=1)
name = st.text_input("Name")
price = st.number_input("Price", min_value=0.0, step=0.01)

if st.button("Add Item"):
    data = {"name": name, "price": price}
    response = requests.post(f"{api_url}/{item_id}", json=data)
    st.write(response.json())

# Get item
st.header("Get Item")
get_id = st.number_input("Item ID to fetch", min_value=1, step=1, key="get")
if st.button("Fetch Item"):
    response = requests.get(f"{api_url}/{get_id}")
    st.write(response.json())