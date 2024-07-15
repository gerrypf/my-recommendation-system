from flask import Flask

app = Flask(__name__)

# Import routes to register them with the Flask application
from app import routes
