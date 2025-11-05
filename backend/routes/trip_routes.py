from flask import Blueprint, request, jsonify, session
import os
import sqlite3

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