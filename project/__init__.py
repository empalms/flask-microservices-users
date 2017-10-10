import os
import datetime
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy

# instantiate the application
app = Flask(__name__)

# Set config
app_settings = os.getenv('APP_SETTINGS')  # pull in environment variables
app.config.from_object('project.config.DevelopmentConfig') # set configuration from config.py


# instantiate the database
db = SQLAlchemy(app)

# user model
class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(128), nullable=False)
    active = db.Column(db.Boolean(), default=False, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)

    def __init__(self, username, email):
        self.username = username
        self.email = email
        self.created_at = datetime.datetime.utcnow()

# routes

@app.route('/ping', methods=['GET'])
def ping_pong():
    return jsonify({
        'status': 'success',
        'message': 'pong!'
})
