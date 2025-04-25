import streamlit as st
import pandas as pd
from database import get_db_connection
from crud import (
    get_all_fruits,
    get_fruit_by_id,
    add_fruit,
    update_fruit,
    delete_fruit
)

# Set page configuration
st.set_page_config(
    page_title="Fruit Storage Management",
    page_icon="🍎",
    layout="wide"
)

# Initialize database
conn = get_db_connection()

# App title
st.title("🍎 Fruit Storage Management System")

# Sidebar for navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["View Inventory", "Add Fruit", "Update Fruit", "Delete Fruit"])

# View Inventory Page
if page == "View Inventory":
    st.header("Fruit Inventory")
    
    # Refresh button
    if st.button("Refresh Data"):
        st.experimental_rerun()
    
    # Get all fruits
    fruits = get_all_fruits(conn)
    
    if fruits:
        # Convert to DataFrame for better display
        df = pd.DataFrame(fruits, columns=["ID", "Name", "Quantity", "Price", "Storage Location", "Expiry Date", "Added Date"])
        st.dataframe(df, use_container_width=True)
        
        # Show total inventory value
        total_value = sum(row[2] * row[3] for row in fruits)  # quantity * price
        st.metric("Total Inventory Value", f"${total_value:.2f}")
        
        # Show expiring soon
        import datetime
        today = datetime.datetime.now().date()
        week_later = today + datetime.timedelta(days=7)
        
        expiring_soon = [fruit for fruit in fruits if fruit[5] and 
                        datetime.datetime.strptime(fruit[5], "%Y-%m-%d").date() <= week_later]
        
        if expiring_soon:
            st.warning(f"⚠️ {len(expiring_soon)} fruits are expiring within a week!")
            exp_df = pd.DataFrame(expiring_soon, columns=["ID", "Name", "Quantity", "Price", "Storage Location", "Expiry Date", "Added Date"])
            st.dataframe(exp_df, use_container_width=True)
    else:
        st.info("No fruits in inventory. Add some fruits!")

# Add Fruit Page
elif page == "Add Fruit":
    st.header("Add New Fruit")
    
    with st.form("add_fruit_form"):
        name = st.text_input("Fruit Name")
        quantity = st.number_input("Quantity", min_value=1, value=1)
        price = st.number_input("Price per Unit ($)", min_value=0.01, value=1.00, format="%.2f")
        location = st.text_input("Storage Location")
        expiry_date = st.date_input("Expiry Date")
        
        submitted = st.form_submit_button("Add Fruit")
        
        if submitted:
            if name and quantity and price and location:
                # Convert date to string format
                expiry_date_str = expiry_date.strftime("%Y-%m-%d")
                
                # Add fruit to database
                success = add_fruit(conn, name, quantity, price, location, expiry_date_str)
                
                if success:
                    st.success(f"Successfully added {name} to inventory!")
                    st.balloons()
                else:
                    st.error("Failed to add fruit. Please try again.")
            else:
                st.warning("Please fill in all required fields.")

# Update Fruit Page
elif page == "Update Fruit":
    st.header("Update Fruit Information")
    
    # Get all fruits for selection
    fruits = get_all_fruits(conn)
    
    if not fruits:
        st.info("No fruits in inventory to update.")
    else:
        # Create a selection box with fruit names and IDs
        fruit_options = {f"{fruit[0]}: {fruit[1]}": fruit[0] for fruit in fruits}
        selected_fruit = st.selectbox("Select Fruit to Update", list(fruit_options.keys()))
        
        # Get the selected fruit ID
        fruit_id = fruit_options[selected_fruit]
        
        # Get current fruit data
        fruit_data = get_fruit_by_id(conn, fruit_id)
        
        if fruit_data:
            with st.form("update_fruit_form"):
                name = st.text_input("Fruit Name", value=fruit_data[1])
                quantity = st.number_input("Quantity", min_value=1, value=fruit_data[2])
                price = st.number_input("Price per Unit ($)", min_value=0.01, value=fruit_data[3], format="%.2f")
                location = st.text_input("Storage Location", value=fruit_data[4])
                
                # Handle expiry date
                if fruit_data[5]:
                    import datetime
                    expiry_date = st.date_input("Expiry Date", 
                                              value=datetime.datetime.strptime(fruit_data[5], "%Y-%m-%d").date())
                else:
                    expiry_date = st.date_input("Expiry Date")
                
                submitted = st.form_submit_button("Update Fruit")
                
                if submitted:
                    if name and quantity and price and location:
                        # Convert date to string format
                        expiry_date_str = expiry_date.strftime("%Y-%m-%d")
                        
                        # Update fruit in database
                        success = update_fruit(conn, fruit_id, name, quantity, price, location, expiry_date_str)
                        
                        if success:
                            st.success(f"Successfully updated {name}!")
                        else:
                            st.error("Failed to update fruit. Please try again.")
                    else:
                        st.warning("Please fill in all required fields.")

# Delete Fruit Page
elif page == "Delete Fruit":
    st.header("Delete Fruit")
    
    # Get all fruits for selection
    fruits = get_all_fruits(conn)
    
    if not fruits:
        st.info("No fruits in inventory to delete.")
    else:
        # Create a selection box with fruit names and IDs
        fruit_options = {f"{fruit[0]}: {fruit[1]} (Qty: {fruit[2]})": fruit[0] for fruit in fruits}
        selected_fruit = st.selectbox("Select Fruit to Delete", list(fruit_options.keys()))
        
        # Get the selected fruit ID
        fruit_id = fruit_options[selected_fruit]
        
        # Confirm deletion
        if st.button("Delete Fruit", type="primary"):
            confirm = st.checkbox("I confirm I want to delete this fruit")
            
            if confirm:
                success = delete_fruit(conn, fruit_id)
                
                if success:
                    st.success(f"Successfully deleted {selected_fruit.split(':')[1].strip().split(' ')[0]}!")
                    # Refresh the page after deletion
                    st.experimental_rerun()
                else:
                    st.error("Failed to delete fruit. Please try again.")
            else:
                st.warning("Please confirm deletion.")

# Footer
st.sidebar.markdown("---")
st.sidebar.info("Fruit Storage Management System v1.0")