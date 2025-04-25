import sqlite3
import os
from pathlib import Path

# Ensure data directory exists
def ensure_data_dir():
    data_dir = Path("data")
    data_dir.mkdir(exist_ok=True)
    return data_dir

# Database connection function
def get_db_connection():
    data_dir = ensure_data_dir()
    db_path = data_dir / "fruits.db"
    
    # Create a connection to the database
    conn = sqlite3.connect(db_path, check_same_thread=False)
    
    # Enable foreign keys
    conn.execute("PRAGMA foreign_keys = ON")
    
    # Create tables if they don't exist
    create_tables(conn)
    
    return conn

# Create database tables
def create_tables(conn):
    cursor = conn.cursor()
    
    # Create fruits table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS fruits (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        quantity INTEGER NOT NULL,
        price REAL NOT NULL,
        storage_location TEXT NOT NULL,
        expiry_date TEXT,
        added_date TEXT DEFAULT CURRENT_DATE
    )
    ''')
    
    # Create a table for fruit categories (for future expansion)
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS categories (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL UNIQUE
    )
    ''')
    
    # Create a table for fruit-category relationships (for future expansion)
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS fruit_categories (
        fruit_id INTEGER,
        category_id INTEGER,
        PRIMARY KEY (fruit_id, category_id),
        FOREIGN KEY (fruit_id) REFERENCES fruits (id) ON DELETE CASCADE,
        FOREIGN KEY (category_id) REFERENCES categories (id) ON DELETE CASCADE
    )
    ''')
    
    # Commit the changes
    conn.commit()

# Initialize the database with some sample data if it's empty
def initialize_sample_data():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Check if the fruits table is empty
    cursor.execute("SELECT COUNT(*) FROM fruits")
    count = cursor.fetchone()[0]
    
    if count == 0:
        # Add some sample fruits
        sample_fruits = [
            ('Apple', 100, 0.50, 'Cold Storage A', '2023-12-31'),
            ('Banana', 150, 0.30, 'Room Temperature Storage', '2023-11-15'),
            ('Orange', 80, 0.60, 'Cold Storage B', '2023-12-20'),
            ('Strawberry', 50, 1.20, 'Freezer', '2023-11-10'),
            ('Mango', 30, 1.50, 'Room Temperature Storage', '2023-11-25')
        ]
        
        cursor.executemany(
            "INSERT INTO fruits (name, quantity, price, storage_location, expiry_date) VALUES (?, ?, ?, ?, ?)",
            sample_fruits
        )
        
        # Add some sample categories
        sample_categories = [
            ('Citrus',),
            ('Tropical',),
            ('Berries',),
            ('Core Fruits',)
        ]
        
        cursor.executemany(
            "INSERT INTO categories (name) VALUES (?)",
            sample_categories
        )
        
        # Add some sample fruit-category relationships
        cursor.execute("SELECT id FROM fruits WHERE name = 'Apple'")
        apple_id = cursor.fetchone()[0]
        
        cursor.execute("SELECT id FROM fruits WHERE name = 'Orange'")
        orange_id = cursor.fetchone()[0]
        
        cursor.execute("SELECT id FROM fruits WHERE name = 'Banana'")
        banana_id = cursor.fetchone()[0]
        
        cursor.execute("SELECT id FROM fruits WHERE name = 'Strawberry'")
        strawberry_id = cursor.fetchone()[0]
        
        cursor.execute("SELECT id FROM fruits WHERE name = 'Mango'")
        mango_id = cursor.fetchone()[0]
        
        cursor.execute("SELECT id FROM categories WHERE name = 'Citrus'")
        citrus_id = cursor.fetchone()[0]
        
        cursor.execute("SELECT id FROM categories WHERE name = 'Tropical'")
        tropical_id = cursor.fetchone()[0]
        
        cursor.execute("SELECT id FROM categories WHERE name = 'Berries'")
        berries_id = cursor.fetchone()[0]
        
        cursor.execute("SELECT id FROM categories WHERE name = 'Core Fruits'")
        core_id = cursor.fetchone()[0]
        
        sample_relationships = [
            (apple_id, core_id),
            (orange_id, citrus_id),
            (banana_id, tropical_id),
            (strawberry_id, berries_id),
            (mango_id, tropical_id)
        ]
        
        cursor.executemany(
            "INSERT INTO fruit_categories (fruit_id, category_id) VALUES (?, ?)",
            sample_relationships
        )
        
        # Commit the changes
        conn.commit()
    
    conn.close()

# Initialize the database with sample data when the module is imported
initialize_sample_data()