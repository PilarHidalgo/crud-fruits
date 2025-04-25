import sqlite3
from typing import List, Tuple, Optional, Any
from datetime import datetime

# Create operations
def add_fruit(conn: sqlite3.Connection, name: str, quantity: int, price: float, 
              storage_location: str, expiry_date: Optional[str] = None) -> bool:
    """
    Add a new fruit to the database.
    
    Args:
        conn: SQLite database connection
        name: Name of the fruit
        quantity: Quantity of the fruit
        price: Price per unit
        storage_location: Where the fruit is stored
        expiry_date: When the fruit expires (YYYY-MM-DD)
        
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO fruits (name, quantity, price, storage_location, expiry_date)
            VALUES (?, ?, ?, ?, ?)
            """,
            (name, quantity, price, storage_location, expiry_date)
        )
        conn.commit()
        return True
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return False

def add_category(conn: sqlite3.Connection, name: str) -> bool:
    """
    Add a new category to the database.
    
    Args:
        conn: SQLite database connection
        name: Name of the category
        
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO categories (name)
            VALUES (?)
            """,
            (name,)
        )
        conn.commit()
        return True
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return False

def assign_fruit_to_category(conn: sqlite3.Connection, fruit_id: int, category_id: int) -> bool:
    """
    Assign a fruit to a category.
    
    Args:
        conn: SQLite database connection
        fruit_id: ID of the fruit
        category_id: ID of the category
        
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO fruit_categories (fruit_id, category_id)
            VALUES (?, ?)
            """,
            (fruit_id, category_id)
        )
        conn.commit()
        return True
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return False

# Read operations
def get_all_fruits(conn: sqlite3.Connection) -> List[Tuple]:
    """
    Get all fruits from the database.
    
    Args:
        conn: SQLite database connection
        
    Returns:
        List of tuples containing fruit data
    """
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT id, name, quantity, price, storage_location, expiry_date, added_date
        FROM fruits
        ORDER BY name
        """
    )
    return cursor.fetchall()

def get_fruit_by_id(conn: sqlite3.Connection, fruit_id: int) -> Optional[Tuple]:
    """
    Get a fruit by its ID.
    
    Args:
        conn: SQLite database connection
        fruit_id: ID of the fruit to retrieve
        
    Returns:
        Tuple containing fruit data or None if not found
    """
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT id, name, quantity, price, storage_location, expiry_date, added_date
        FROM fruits
        WHERE id = ?
        """,
        (fruit_id,)
    )
    return cursor.fetchone()

def get_fruits_by_category(conn: sqlite3.Connection, category_id: int) -> List[Tuple]:
    """
    Get all fruits in a specific category.
    
    Args:
        conn: SQLite database connection
        category_id: ID of the category
        
    Returns:
        List of tuples containing fruit data
    """
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT f.id, f.name, f.quantity, f.price, f.storage_location, f.expiry_date, f.added_date
        FROM fruits f
        JOIN fruit_categories fc ON f.id = fc.fruit_id
        WHERE fc.category_id = ?
        ORDER BY f.name
        """,
        (category_id,)
    )
    return cursor.fetchall()

def get_all_categories(conn: sqlite3.Connection) -> List[Tuple]:
    """
    Get all categories from the database.
    
    Args:
        conn: SQLite database connection
        
    Returns:
        List of tuples containing category data
    """
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT id, name
        FROM categories
        ORDER BY name
        """
    )
    return cursor.fetchall()

def get_expiring_fruits(conn: sqlite3.Connection, days: int = 7) -> List[Tuple]:
    """
    Get fruits that will expire within the specified number of days.
    
    Args:
        conn: SQLite database connection
        days: Number of days to check for expiration
        
    Returns:
        List of tuples containing fruit data
    """
    cursor = conn.cursor()
    today = datetime.now().date().isoformat()
    cursor.execute(
        """
        SELECT id, name, quantity, price, storage_location, expiry_date, added_date
        FROM fruits
        WHERE expiry_date IS NOT NULL
        AND date(expiry_date) <= date(?, '+' || ? || ' days')
        AND date(expiry_date) >= date(?)
        ORDER BY expiry_date
        """,
        (today, days, today)
    )
    return cursor.fetchall()

def search_fruits(conn: sqlite3.Connection, search_term: str) -> List[Tuple]:
    """
    Search for fruits by name or storage location.
    
    Args:
        conn: SQLite database connection
        search_term: Term to search for
        
    Returns:
        List of tuples containing fruit data
    """
    cursor = conn.cursor()
    search_pattern = f"%{search_term}%"
    cursor.execute(
        """
        SELECT id, name, quantity, price, storage_location, expiry_date, added_date
        FROM fruits
        WHERE name LIKE ? OR storage_location LIKE ?
        ORDER BY name
        """,
        (search_pattern, search_pattern)
    )
    return cursor.fetchall()

# Update operations
def update_fruit(conn: sqlite3.Connection, fruit_id: int, name: str, quantity: int, 
                price: float, storage_location: str, expiry_date: Optional[str] = None) -> bool:
    """
    Update an existing fruit in the database.
    
    Args:
        conn: SQLite database connection
        fruit_id: ID of the fruit to update
        name: New name of the fruit
        quantity: New quantity of the fruit
        price: New price per unit
        storage_location: New storage location
        expiry_date: New expiry date (YYYY-MM-DD)
        
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        cursor = conn.cursor()
        cursor.execute(
            """
            UPDATE fruits
            SET name = ?, quantity = ?, price = ?, storage_location = ?, expiry_date = ?
            WHERE id = ?
            """,
            (name, quantity, price, storage_location, expiry_date, fruit_id)
        )
        conn.commit()
        return cursor.rowcount > 0
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return False

def update_fruit_quantity(conn: sqlite3.Connection, fruit_id: int, quantity: int) -> bool:
    """
    Update only the quantity of a fruit.
    
    Args:
        conn: SQLite database connection
        fruit_id: ID of the fruit to update
        quantity: New quantity of the fruit
        
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        cursor = conn.cursor()
        cursor.execute(
            """
            UPDATE fruits
            SET quantity = ?
            WHERE id = ?
            """,
            (quantity, fruit_id)
        )
        conn.commit()
        return cursor.rowcount > 0
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return False

def update_category(conn: sqlite3.Connection, category_id: int, name: str) -> bool:
    """
    Update a category name.
    
    Args:
        conn: SQLite database connection
        category_id: ID of the category to update
        name: New name of the category
        
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        cursor = conn.cursor()
        cursor.execute(
            """
            UPDATE categories
            SET name = ?
            WHERE id = ?
            """,
            (name, category_id)
        )
        conn.commit()
        return cursor.rowcount > 0
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return False

# Delete operations
def delete_fruit(conn: sqlite3.Connection, fruit_id: int) -> bool:
    """
    Delete a fruit from the database.
    
    Args:
        conn: SQLite database connection
        fruit_id: ID of the fruit to delete
        
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        cursor = conn.cursor()
        cursor.execute(
            """
            DELETE FROM fruits
            WHERE id = ?
            """,
            (fruit_id,)
        )
        conn.commit()
        return cursor.rowcount > 0
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return False

def delete_category(conn: sqlite3.Connection, category_id: int) -> bool:
    """
    Delete a category from the database.
    
    Args:
        conn: SQLite database connection
        category_id: ID of the category to delete
        
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        cursor = conn.cursor()
        cursor.execute(
            """
            DELETE FROM categories
            WHERE id = ?
            """,
            (category_id,)
        )
        conn.commit()
        return cursor.rowcount > 0
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return False

def remove_fruit_from_category(conn: sqlite3.Connection, fruit_id: int, category_id: int) -> bool:
    """
    Remove a fruit from a category.
    
    Args:
        conn: SQLite database connection
        fruit_id: ID of the fruit
        category_id: ID of the category
        
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        cursor = conn.cursor()
        cursor.execute(
            """
            DELETE FROM fruit_categories
            WHERE fruit_id = ? AND category_id = ?
            """,
            (fruit_id, category_id)
        )
        conn.commit()
        return cursor.rowcount > 0
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return False