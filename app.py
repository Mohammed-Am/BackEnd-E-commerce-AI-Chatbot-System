from flask import Flask
from flask_cors import CORS
from flask_caching import Cache
from flasgger import Swagger
from controllers.routes import main_bp

app = Flask(__name__)

CORS(app) 

# Configure cache
app.config['CACHE_TYPE'] = 'simple'
cache = Cache(app)

# Configure Swagger
swagger = Swagger(app)

app.register_blueprint(main_bp)

