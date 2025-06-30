from bson.objectid import ObjectId

class Product:
    def __init__(self, db):
        self.collection = db.products

    def get_all(self):
        products = list(self.collection.find())
        for product in products:
            product['_id'] = str(product['_id'])
        return products

    def get_one(self, product_id):
        product = self.collection.find_one({'_id': ObjectId(product_id)})
        if product:
            product['_id'] = str(product['_id'])
        return product

    def create(self, product_data):
        result = self.collection.insert_one(product_data)
        return str(result.inserted_id)

    def delete_all(self):
        self.collection.delete_many({})
