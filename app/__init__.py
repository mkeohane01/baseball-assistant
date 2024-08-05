from flask import Flask
from .routes import app as routes_blueprint
from src.populate_db import update_pitching_stats, update_hitting_stats

def create_app():
    app = Flask(__name__)

    # Register blueprints
    app.register_blueprint(routes_blueprint)

    # Populate the database when the app is created
    update_pitching_stats()
    update_hitting_stats()

    return app

#if you want to run the app directly from this file
if __name__ == "__main__":
    app = create_app()
    app.run()
