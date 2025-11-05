"""
Initialize database.
Creates tables
"""

from datetime import datetime
import json
import sqlite3

def create_tables(conn):
    """Create all database tables if they don't already exist"""

    cursor = conn.cursor()
    tables = [
        '''CREATE TABLE IF NOT EXISTS trips (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tripName TEXT,
            tripType TEXT NOT NULL DEFAULT 'hiking'
                CHECK (tripType IN ('hiking', 'climbing', 'social', 'skiing', 'boating', 'other')),
            tripDate TEXT,
            tripLeader TEXT,
            tripLocation TEXT,
            info TEXT,
            link TEXT,
            formCloseDate TEXT,
            isFormClosed INTEGER CHECK (isFormClosed BETWEEN 0 AND 1)
        )''',
        '''CREATE TABLE IF NOT EXISTS gear (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            gearName TEXT,
            discipline TEXT,
            availability INTEGER CHECK (availability BETWEEN 0 AND 1)
        )'''
    ]

    for table in tables:
        cursor.execute(table)
    conn.commit()

if __name__ == "__main__":
    db_conn = sqlite3.connect('ucoc.db')
    create_tables(db_conn)
    db_conn.close()