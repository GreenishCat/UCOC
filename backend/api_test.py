"""
Test module for UCOC API endpoints
"""
# pylint: disable=redefined-outer-name
import os
import sqlite3
import pytest
from main import app
from init_db import CreateTables, InsertTestData

TEST_DB = 'ucoc.db'

# pylint: disable=duplicate-code
@pytest.fixture(scope='module')
def client():
    """Fixture to setup test client with test db"""
    if os.path.exists(TEST_DB): os.remove(TEST_DB)

    conn = sqlite3.connect(TEST_DB)
    CreateTables(conn)
    InsertTestData(conn)
    conn.close()

    app.testing = True

    yield app.test_client()

    if os.path.exists(TEST_DB): os.remove(TEST_DB) #remove test db

def test_create_trip(client):
    """Test creating a new trip"""

    test_values = {
        "tripName": "TikTok Rizz Party",
        "tripDate": "2026-02-14",
        "tripLeader": "Jerma",
        "tripLocation": "Agartha",
        "info": "Sorry you had to read this...",
        "link": "https://www.google.com",
        "formCloseDate": "2026-02-11T16:20",
        "isFormClosed": 0
    }

    #Test complete addition
    testCreate = client.post('/trips/create', json=test_values)
    assert testCreate.status_code == 201
    assert testCreate.json['trip']['tripLeader'] == "Jerma"

    #Test incomplete addition
    # test_values = {"tripName": "Nothing else here!"}

    # testCreate = client.post('/trips/create', json=test_values)
    # assert testCreate.status_code == 400


def test_get_all_trips(client):
    """Test get all trips"""

    response = client.get('/trips/all')

    assert response.status_code == 200
    assert response.json['count'] == 3

    assert len(response.json['trips']) == 3

def test_get_current_trips(client):
    """Test get current trips"""

    response = client.get('/trips')

    assert response.status_code == 200
    assert response.json['count'] == 2

    assert len(response.json['trips']) == 2