"""
Initialize database.
Creates tables
"""

from datetime import datetime
import json
import sqlite3

def CreateTables(conn):
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
        )''',
        '''CREATE TABLE IF NOT EXISTS gearRequest (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            email TEXT,
            phoneNumber TEXT,
            items TEXT,
            quantity TEXT,
            period TEXT,
            status TEXT NOT NULL DEFAULT 'pending'
                CHECK (status IN ('pending', 'accepted', 'rejected')),
            date TEXT
        )''',
        '''CREATE TABLE IF NOT EXISTS news (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            eventName TEXT,
            content TEXT,
            thumbnail TEXT,
            expireDate TEXT,
            date TEXT
        )''',
        '''CREATE TABLE IF NOT EXISTS leaders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            position TEXT NOT NULL DEFAULT 'member'
                CHECK (position IN ('member', 'president', 'vicePresident', 'treasurer', 'secretary', 'outreach', 'gearManager')),
            pictureURL TEXT,
            info TEXT,
            date TEXT
        )'''
    ]

    for table in tables:
        cursor.execute(table)
    conn.commit()

def InsertTestData(conn):
    """Insert test data into the database"""
    cursor = conn.cursor()

    #Current EBoard
    cursor.executemany('''
        INSERT INTO leaders (name, position, pictureURL, info, date)
        VALUES (?, ?, ?, ?, ?)
    ''', [
        ('Gio Girasoli', 'president', 'x', 'I like long walks on the beach and playing Minecraft', datetime.now().isoformat(timespec='hours')),
        ('Sydney Kolz', 'vicePresident', 'x', 'x', datetime.now().isoformat(timespec='hours')),
        ('Ryan Le Vine', 'treasurer', 'x', 'x', datetime.now().isoformat(timespec='hours')),
        ('Ginny Decker', 'secretary', 'x', 'x', datetime.now().isoformat(timespec='hours')),
        ('Parker Pretty', 'outreach', 'x', 'x', datetime.now().isoformat(timespec='hours'))
    ])

    #Example Trip
    cursor.executemany('''
        INSERT INTO trips (tripName, tripType, tripDate, tripLeader, tripLocation, info, link, formCloseDate, isFormClosed)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', [
        ('Mt. Washington', 'hiking', '2025-09-05', 'EBoard', 'Mt. Washington', 'Everybody\'s favorite', 'x', datetime.now().isoformat(timespec='hours'), 1)
    ])

    conn.commit()

if __name__ == "__main__":
    db_conn = sqlite3.connect('ucoc.db')
    CreateTables(db_conn)
    InsertTestData(db_conn)
    db_conn.close()