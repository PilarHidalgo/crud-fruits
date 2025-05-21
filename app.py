import streamlit as st
import json
import os
import uuid
from datetime import datetime

#test codegpt
st.set_page_config(
    page_title="Fruit Store CRUD",
    page_icon="🍎",
    layout="wide"
)


DATA_DIR = "data"
DATA_FILE = os.path.join(DATA_DIR, "fruits.json")


if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)


def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return []
    else:
        # Create empty file if it doesn't exist
        with open(DATA_FILE, "w") as f:
            json.dump([], f)
        return []


def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)


if 'fruits' not in st.session_state:
    st.session_state.fruits = load_data()
if 'edit_mode' not in st.session_state:
    st.session_state.edit_mode = False
if 'edit_id' not in st.session_state:
    st.session_state.edit_id = None


st.title("🍎 Fruit Store Inventory Management")


with st.sidebar:
    st.header("Add/Edit Fruit")
    
    # Form for adding/editing fruits
    with st.form(key="fruit_form"):
        name = st.text_input("Fruit Name", key="name")
        price = st.number_input("Price ($)", min_value=0.01, step=0.01, key="price")
        quantity = st.number_input("Quantity", min_value=1, step=1, key="quantity")
        category = st.selectbox("Category", ["Fresh", "Frozen", "Dried", "Exotic"], key="category")
        description = st.text_area("Description", key="description")
        
        submit_button = st.form_submit_button(
            "Update Fruit" if st.session_state.edit_mode else "Add Fruit"
        )
        
        if submit_button:
            if not name:
                st.error("Fruit name cannot be empty!")
            else:
                if st.session_state.edit_mode:
                    # Update existing fruit
                    for i, fruit in enumerate(st.session_state.fruits):
                        if fruit["id"] == st.session_state.edit_id:
                            st.session_state.fruits[i] = {
                                "id": st.session_state.edit_id,
                                "name": name,
                                "price": price,
                                "quantity": quantity,
                                "category": category,
                                "description": description,
                                "updated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                            }
                            break
                    st.session_state.edit_mode = False
                    st.session_state.edit_id = None
                    st.success(f"Updated {name} successfully!")
                else:
                    # Add new fruit
                    new_fruit = {
                        "id": str(uuid.uuid4()),
                        "name": name,
                        "price": price,
                        "quantity": quantity,
                        "category": category,
                        "description": description,
                        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "updated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    }
                    st.session_state.fruits.append(new_fruit)
                    st.success(f"Added {name} successfully!")
                
                # Save data to file
                save_data(st.session_state.fruits)
                
                # Clear form fields
                st.session_state.name = ""
                st.session_state.price = 0.01
                st.session_state.quantity = 1
                st.session_state.category = "Fresh"
                st.session_state.description = ""
    
    if st.session_state.edit_mode:
        if st.button("Cancel Edit"):
            st.session_state.edit_mode = False
            st.session_state.edit_id = None
            st.session_state.name = ""
            st.session_state.price = 0.01
            st.session_state.quantity = 1
            st.session_state.category = "Fresh"
            st.session_state.description = ""
            st.experimental_rerun()


st.header("Fruit Inventory")


search_term = st.text_input("Search fruits", "")


filtered_fruits = st.session_state.fruits
if search_term:
    filtered_fruits = [
        fruit for fruit in st.session_state.fruits
        if search_term.lower() in fruit["name"].lower() or 
           search_term.lower() in fruit["category"].lower() or
           search_term.lower() in fruit["description"].lower()
    ]


if not filtered_fruits:
    st.info("No fruits in inventory. Add some from the sidebar!")
else:
    # Create columns for the table header
    col1, col2, col3, col4, col5, col6 = st.columns([2, 1, 1, 1, 3, 2])
    col1.markdown("**Name**")
    col2.markdown("**Price**")
    col3.markdown("**Quantity**")
    col4.markdown("**Category**")
    col5.markdown("**Description**")
    col6.markdown("**Actions**")
    
    st.markdown("---")
    
    # Display each fruit
    for fruit in filtered_fruits:
        col1, col2, col3, col4, col5, col6 = st.columns([2, 1, 1, 1, 3, 2])
        col1.write(fruit["name"])
        col2.write(f"${fruit['price']:.2f}")
        col3.write(fruit["quantity"])
        col4.write(fruit["category"])
        col5.write(fruit["description"][:50] + "..." if len(fruit["description"]) > 50 else fruit["description"])
        
        # Edit and Delete buttons
        edit_button = col6.button("Edit", key=f"edit_{fruit['id']}")
        delete_button = col6.button("Delete", key=f"delete_{fruit['id']}")
        
        if edit_button:
            # Set edit mode and populate form with fruit data
            st.session_state.edit_mode = True
            st.session_state.edit_id = fruit["id"]
            st.session_state.name = fruit["name"]
            st.session_state.price = fruit["price"]
            st.session_state.quantity = fruit["quantity"]
            st.session_state.category = fruit["category"]
            st.session_state.description = fruit["description"]
            st.experimental_rerun()
        
        if delete_button:
            # Remove fruit from list
            st.session_state.fruits = [f for f in st.session_state.fruits if f["id"] != fruit["id"]]
            save_data(st.session_state.fruits)
            st.success(f"Deleted {fruit['name']} successfully!")
            st.experimental_rerun()
        
        st.markdown("---")


if st.session_state.fruits:
    st.header("Inventory Statistics")
    
    col1, col2, col3 = st.columns(3)
    
    
    col1.metric("Total Fruit Types", len(st.session_state.fruits))
    
   
    total_value = sum(fruit["price"] * fruit["quantity"] for fruit in st.session_state.fruits)
    col2.metric("Total Inventory Value", f"${total_value:.2f}")
    
   
    total_quantity = sum(fruit["quantity"] for fruit in st.session_state.fruits)
    col3.metric("Total Fruit Items", total_quantity)
    
    
    st.subheader("Category Distribution")
    category_counts = {}
    for fruit in st.session_state.fruits:
        category = fruit["category"]
        if category in category_counts:
            category_counts[category] += 1
        else:
            category_counts[category] = 1
    
    st.bar_chart(category_counts)

# Footer
st.markdown("---")
st.markdown("© 2023 Fruit Store CRUD App | Built with Streamlit")
