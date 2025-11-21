"""
Main executable for the UCOC website API
Initializes Flask app
"""

from flask import Flask
from flask_cors import CORS
from flasgger import Swagger
from init_db import CreateTables, InsertTestData
# API
from routes.trip_routes import trips_bp

TEST_DB = 'ucoc.db'

app = Flask(__name__)
app.secret_key = 'iminsecure'

CORS(app, supports_credentials=True, origins=["http://localhost:5173"])
swagger = Swagger(app)

app.register_blueprint(trips_bp)

@app.route('/')
def index():
    return "<h1>Your baby thinks that people can't change</h1>"

def initializeDB():
    if os.path.exists(TEST_DB): os.remove(TEST_DB)

    conn = sqlite3.connect(TEST_DB)
    CreateTables(conn)
    InsertTestData(conn)
    conn.close()

if __name__ == '__main__':
    initializeDB()
    app.run(host="0.0.0.0", port=5000)
