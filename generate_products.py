
import json
import random

def generate_products():
    """Generates a list of 50 realistic bike products and saves them to a JSON file."""
    
    brands = ["Trek", "Specialized", "Giant", "Cannondale", "Scott", "Santa Cruz", "Rad Power", "Canyon"]
    types = {
        "Mountain": ["Marlin", "Stumpjumper", "Trance", "Habit", "Spark", "Tallboy"],
        "Road": ["Domane", "Allez", "Defy", "Synapse", "Addict", "Aeroad"],
        "Hybrid": ["FX", "Sirrus", "Escape", "Quick", "Sub Sport", "Pathlite"],
        "Electric": ["Powerfly", "Turbo Levo", "Explore E+", "Topstone Neo", "Strike eRIDE", "Heckler"]
    }
    adjectives = ["Pro", "Comp", "Expert", "SL", "LTD", "EVO", "AL", "CF"]
    colors = ["Red", "Blue", "Black", "Silver", "Green", "White", "Orange"]
    
    products = []
    
    for i in range(50): # Changed to 50 products
        bike_type = random.choice(list(types.keys()))
        brand = random.choice(brands)
        model_base = random.choice(types[bike_type])
        adjective = random.choice(adjectives)
        color = random.choice(colors)
        
        name = f"{brand} {model_base} {adjective} {i+1}"
        
        if bike_type == "Mountain":
            price = round(random.uniform(800, 5000), 2)
            desc = f"A durable {bike_type.lower()} bike designed for rugged trails. Features a lightweight {brand.lower()} frame, advanced suspension, and a modern geometry for confident handling."
        elif bike_type == "Road":
            price = round(random.uniform(1000, 7000), 2)
            desc = f"An aerodynamic {bike_type.lower()} bike built for speed and efficiency on the pavement. Perfect for racing, group rides, or long solo adventures."
        elif bike_type == "Hybrid":
            price = round(random.uniform(500, 1500), 2)
            desc = f"A versatile {bike_type.lower()} bike that's perfect for city commuting, fitness rides, and weekend explorations on bike paths."
        else: # Electric
            price = round(random.uniform(1500, 8000), 2)
            desc = f"A powerful {bike_type.lower()} bike that gives you an extra boost on climbs and long rides. Features a long-lasting battery and an intuitive pedal-assist system."

        product = {
            "name": name,
            "type": bike_type, # Added type field
            "price": price,
            "description": f"{desc} Comes in a stylish {color} finish.",
            "image_url": f"https://placehold.co/600x400/CCCCCC/000000?text={brand.replace(' ', '+')}",
            "amazon_link": f"https://www.amazon.com/s?k={name.replace(' ', '+')}" # Added amazon_link
        }
        products.append(product)
        
    with open("products.json", "w") as f:
        json.dump(products, f, indent=4)
        
    print("Successfully generated 50 products and saved to products.json")

if __name__ == "__main__":
    generate_products()
