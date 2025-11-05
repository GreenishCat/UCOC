"""
Main executable for the UCOC website API
Initializes Flask app
"""

from flask import Flask
from flask_cors import CORS
from flasgger import Swagger

app = Flask(__name__)
app.secret_key = 'iminsecure'

CORS(app, supports_credentials=True, origins=["http://localhost:5173"])

swagger = Swagger(app)

@app.route('/')
def index():
    return "<h1>Your baby thinks that people can't change</h1>"

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)