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

    try:
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
    except Exception as e:
        cursor.close()
        conn.close()
        return jsonify({
            "error": "Failed to get current trips",
            "details": str(e)
        }), 500

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

    try:
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
    except Exception as e:
        cursor.close()
        conn.close()
        return jsonify({
            "error": "Failed to get all trips",
            "details": str(e)
        }), 500

@trips_bp.route('/trips/create', methods=['POST'])
def CreateTrip():
    """
    Create a trip
    ---
    tags:
      - Trips

    parameters:
      - in: body
        name: Trip Data
        description: Required fields: tripName, tripDate, tripLeader, tripLocation, info, link, formCloseDate, isFormClosed
        required: true
        schema:
            type: object
            required:
                - tripName
                - tripDate
                - tripLeader
                - tripLocation
                - info
                - link
                - formCloseDate
                - isFormClosed
            properties:
                tripName:
                    type: string
                    example: "Mt. Washington"
                tripDate:
                    type: string
                    example: "2025-12-18" (ISO yyyy-mm-dd)
                tripLeader:
                    type: string
                    example: "EBoard"
                tripLocation:
                    type: string
                    example: "Mt. Washington"
                info:
                    type: string
                    example: "Annual first trip"
                link:
                    type: string
                    example: "https://forms.office.com/x"
                formCloseDate:
                    type: string
                    example: "2025-12-18T16:20"
                isFormClosed:
                    type: boolean
                    example: 0

    responses:
        201:
            description: Trip created successfully
        400:
            description: Missing required fields
    """

    conn = GetDBConnection()
    cursor = conn.cursor()

    data = request.json
    required_fields = ['tripName', 'tripDate', 'tripLeader', 'tripLocation', 'info', 'link', 'formCloseDate', 'isFormClosed']

    missing_fields = [field for field in required_fields if field not in data or not data[field]]
    if missing_fields:
        return jsonify({
            "error": "Missing required fields",
            "missing_fields": missing_fields
        }), 400
    
    try:
        cursor.execute('''
            INSERT INTO trips (
                tripName, tripDate, tripLeader, tripLocation, info, link, formCloseDate, isFormClosed           
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            data['tripName'],
            data['tripDate'],
            data['tripLeader'],
            data['tripLocation'],
            data['info'],
            data['link'],
            data['formCloseDate'],
            data['isFormClosed']
        ))
        conn.commit()
        newTripID = cursor.lastrowid
        cursor.close()
        conn.close()

        return jsonify({
            "message": "Trip created successfully",
            "newTripID": newTripID
        }), 201
    except Exception as e:
        cursor.close()
        conn.close()
        return jsonify({
            "error": "Failed to create trip",
            "details": str(e)
        }), 500

