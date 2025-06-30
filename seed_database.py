import json
import requests
import time
import os
from models.product import Product
from config.db import get_db

API_URL = "http://127.0.0.1:5000/products"

def seed_database():
    """Reads products from products.json and adds them to the database via the API."""
    db = get_db()
    product_model = Product(db)

    print("Clearing existing products from the database...")
    product_model.delete_all()
    print("Existing products cleared.")

    # Construct the absolute path to products.json
    base_dir = os.path.dirname(os.path.abspath(__file__))
    products_file_path = os.path.join(base_dir, '..', 'products.json')

    print(f"Reading products from {products_file_path}...")
    try:
        with open(products_file_path, 'r') as f:
            products_to_add = json.load(f)
    except FileNotFoundError:
        print(f"Error: {products_file_path} not found. Please run generate_products.py first.")
        return
    except json.JSONDecodeError:
        print(f"Error: Could not decode JSON from {products_file_path}. Check file format.")
        return

    if not products_to_add:
        print("No products found in products.json.")
        return

    headers = {"Content-Type": "application/json"}
    success_count = 0
    
    for product in products_to_add:
        try:
            response = requests.post(API_URL, headers=headers, json=product)
            if response.status_code == 201:
                print(f"Successfully added: {product['name']}")
                success_count += 1
            else:
                print(f"Error adding {product['name']}: {response.status_code} - {response.text}")
            
            # Add a small delay to avoid overwhelming your local server
            time.sleep(0.05)
            
        except requests.exceptions.RequestException as e:
            print(f"Error connecting to the API: {e}")
            print("Please make sure the Flask server is running.")
            return
            
    print(f"\nSeeding complete. Successfully added {success_count}/{len(products_to_add)} products.")

if __name__ == "__main__":
    seed_database()

