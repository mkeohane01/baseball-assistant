import sys
import os

# Add the root directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from app import create_app
from src.utils import get_pitching_stats, get_batting_stats


@pytest.fixture(scope='module')
def app():
    app = create_app()
    app.config['TESTING'] = True
    return app

@pytest.fixture(scope='module')
def client(app):
    return app.test_client()

def test_health_endpoint(client):
    response = client.get('/')
    # print(response.data)
    assert response.status_code == 200
    assert b"AI Baseball Chat" in response.data

def test_get_pitching_stats_success():
    status_code, player_stats = get_pitching_stats('Jake Irvin')
    
    assert status_code == 200
    assert player_stats['Name'] == 'Jake Irvin'

def test_get_pitching_stats_not_found():
    status_code, error_message = get_pitching_stats('John Doe')
    
    assert status_code == 404 or status_code == 405
    assert "Unable to find player" in error_message

def test_get_pitching_stats_similar_names():
    status_code, error_message = get_pitching_stats('Jke Irvin')
    
    assert status_code == 405
    assert "Did you mean" in error_message
    assert "Jake Irvin" in error_message

def test_get_batting_stats_success():
    status_code, player_stats = get_batting_stats('CJ Abrams')
    
    assert status_code == 200
    assert player_stats['Name'] == 'CJ Abrams'

def test_get_batting_stats_not_found():
    status_code, error_message = get_batting_stats('John Doe')
    
    assert status_code == 404 or status_code == 405
    assert "Unable to find player" in error_message

def test_get_batting_stats_similar_names():
    status_code, error_message = get_batting_stats('CJ Abrms')
    
    assert status_code == 405
    assert "Did you mean" in error_message
    assert "CJ Abrams" in error_message

if __name__ == '__main__':
    pytest.main()
