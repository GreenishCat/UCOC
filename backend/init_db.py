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

    ]

    for table in tables:
        cursor.execute(table)
    conn.commit()