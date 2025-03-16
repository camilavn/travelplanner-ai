from flask import Flask
from website.views import travel_bp

def create_app():
    app = Flask(__name__)
    app.register_blueprint(travel_bp)
    return app
