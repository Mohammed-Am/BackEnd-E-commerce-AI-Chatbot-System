from flask import Blueprint, request, jsonify
from models.product import Product
from services.gemini_service import generate_response
from config.db import get_db
import json
import re

import os

main_bp = Blueprint('main', __name__)

db = get_db()
product_model = Product(db)

def load_prompt_template(file_path):
    # Construct an absolute path to the file
    # Assuming this script is in backend/controllers and the prompt is in backend/prompts
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    absolute_file_path = os.path.join(base_dir, file_path)
    with open(absolute_file_path, 'r') as f:
        return f.read()

CHAT_PROMPT_TEMPLATE = load_prompt_template('prompts/chat_prompt.txt')

@main_bp.route('/health')
def health_check():
    return "OK", 200

@main_bp.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message')
    if not user_message:
        return jsonify({'error': 'No message provided'}), 400

    products = product_model.get_all()
    
    # Extract budget from user message
    budget = None
    match = re.search(r'\$(\d+)', user_message) # Look for $ followed by digits
    if match:
        try:
            budget = float(match.group(1))
        except ValueError:
            pass # Ignore if conversion fails

    filtered_products = []
    if budget is not None:
        for product in products:
            if product.get('price') is not None and product['price'] <= budget:
                filtered_products.append(product)
    else:
        filtered_products = products # If no budget, consider all products

    # Create a simplified list of products for the prompt
    product_list_for_prompt = [{k: v for k, v in p.items() if k in ['_id', 'name', 'type', 'price', 'description', 'image_url', 'website_link']} for p in filtered_products]

    prompt = CHAT_PROMPT_TEMPLATE.format(
        user_message=user_message,
        product_list_json=json.dumps(product_list_for_prompt, indent=2)
    )

    try:
        ai_response_str = generate_response(prompt)
        # The response from the AI is a JSON string, so we parse it
        ai_response_json = json.loads(ai_response_str)
        return jsonify(ai_response_json)
    except Exception as e:
        print(f"Error processing AI response: {e}")
        # Fallback to a simple text response if JSON parsing fails
        return jsonify({"response": "I'm sorry, I had trouble finding specific products for you right now. Please ask me another question!", "products": []})

@main_bp.route('/products', methods=['POST'])
def add_product():
    product_data = request.json
    if not product_data:
        return jsonify({'error': 'No product data provided'}), 400

    inserted_id = product_model.create(product_data)
    return jsonify({'inserted_id': inserted_id}), 201

@main_bp.route('/products', methods=['GET'])
def get_products():
    products = product_model.get_all()
    return jsonify(products), 200

@main_bp.route('/products/<product_id>', methods=['GET'])
def get_product(product_id):
    product = product_model.get_one(product_id)
    if product:
        return jsonify(product), 200
    else:
        return jsonify({'error': 'Product not found'}), 404
