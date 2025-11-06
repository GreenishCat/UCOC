from flask import Blueprint, request, jsonify, session
import os
import sqlite3
from datetime import datetime

trips_bp = Blueprint('trips', __name__)

def GetDBConnection():
    dbPath = os.path.join(os.path.dirname(__file__), '..', 'ucoc.db')
    conn = sqlite3.connect(dbPath)
    conn.row_factory = sqlite3.Row
    return conn

@trips_bp.route('/trips/<int:trip_id>', methods=['GET'])
def GetTripByID(trip_id):
    """
    Get a trip by integer ID
    ---
    tags:
      - Trips

    parameters:
      - in: path
        name: trip_id
        description: ID of a trip to grab from database
        required: true
        schema:
            type: integer
            example: 1

    responses:
        200:
            description: The trip with a specified id
        404:
            description: No trip by this id
    """

    conn = GetDBConnection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM trips WHERE id = ?",
        (trip_id,)
    )
    trip = cursor.fetchone()
    cursor.close()
    conn.close()

    if not trip:
        conn.close()
        return jsonify({'error': 'Trip not found'}), 404
    
    return jsonify({
        "id": trip["id"],
        "tripName": trip["tripName"],
        "tripDate": trip["tripDate"],
        "tripLeader": trip["tripLeader"],
        "tripLocation": trip["tripLocation"],
        "info": trip["info"],
        "link": trip["link"],
        "formCloseDate": trip["formCloseDate"],
        "isFormClosed": trip["isFormClosed"]
    })

@trips_bp.route('/trips', methods=['GET'])
def GetCurrentTrips():
    """
    Get all current trips (tripDate > current date), ordered by tripDate
    ---
    tags:
      - Trips

    responses:
        200:
            description: The list of current trips
    """

    conn = GetDBConnection()
    cursor = conn.cursor()

    rows = cursor.execute('''
        SELECT * FROM trips WHERE tripDate > ? ORDER BY tripDate DESC
    ''', (datetime.now().isoformat(),)).fetchall()

    tripList = []
    for row in rows:
        tripList.append({
            "id": row[0],
            "tripName": row[1],
            "tripDate": row[2],
            "tripLeader": row[3],
            "tripLocation": row[4],
            "info": row[5],
            "link": row[6],
            "formCloseDate": row[7],
            "isFormClosed": row[8]
        })

    cursor.close()
    conn.close()

    return jsonify({
        "count": len(tripList),
        "trips": tripList
    }), 200

@trips_bp.route('/trips/all', methods=['GET'])
def GetAllTrips():
    """
    Get all trips, ordered by tripDate
    ---
    tags:
      - Trips

    responses:
        200:
            description: The list of all trips
    """

    conn = GetDBConnection()
    cursor = conn.cursor()

    rows = cursor.execute('''
        SELECT * FROM trips ORDER BY tripDate DESC
    ''').fetchall()

    tripList = []
    for row in rows:
        tripList.append({
            "id": row[0],
            "tripName": row[1],
            "tripDate": row[2],
            "tripLeader": row[3],
            "tripLocation": row[4],
            "info": row[5],
            "link": row[6],
            "formCloseDate": row[7],
            "isFormClosed": row[8]
        })

    cursor.close()
    conn.close()

    return jsonify({
        "count": len(tripList),
        "trips": tripList
    }), 200