from flask import Flask

def create_app():
    app = Flask(__name__)
    
    # Import routes
    from app.routes import wildfire_routes
    app.register_blueprint(wildfire_routes)
    
    return app