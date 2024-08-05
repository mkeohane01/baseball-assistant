from flask import Flask
from .routes import app as routes_blueprint
from src.populate_db import update_pitching_stats, update_hitting_stats

def create_app():
    baseball_app = Flask(__name__)

    # Register blueprints
    baseball_app.register_blueprint(routes_blueprint)

    # Populate the database when the app is created
    update_pitching_stats()
    update_hitting_stats()

    return baseball_app

#if you want to run the app directly from this file
if __name__ == "__main__":
    baseball_app = create_app()
    baseball_app.run()
