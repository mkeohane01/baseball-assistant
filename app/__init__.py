from .routes import app
from src.populate_db import update_pitching_stats, update_hitting_stats

def main():
    update_pitching_stats()
    update_hitting_stats()
    app.run()