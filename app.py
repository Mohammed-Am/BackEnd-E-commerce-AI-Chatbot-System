from flask import Flask
from flask_cors import CORS
from flask_caching import Cache
from flasgger import Swagger
from controllers.routes import main_bp

app = Flask(__name__)
# In a production environment, replace '*' with your Vercel frontend domain
# e.g., CORS(app, resources={r"/*": {"origins": "https://your-vercel-app-domain.vercel.app"}})
CORS(app, resources={r"/*": {"origins": "*"}}) # For development flexibility, but restrict in production!

# Configure cache
app.config['CACHE_TYPE'] = 'simple'
cache = Cache(app)

# Configure Swagger
swagger = Swagger(app)

app.register_blueprint(main_bp)

if __name__ == '__main__':
    app.run(debug=True)