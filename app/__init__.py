from flask import Flask
from flask_cors import CORS

def create_app():
    app = Flask(__name__)

    # Enable CORS for all routes
    CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)

    # Import and register routes
    from app.routes import wildfire_routes
    app.register_blueprint(wildfire_routes)

    return app
