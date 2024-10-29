import logging
import os

from dotenv import load_dotenv
from flask import Flask, jsonify
from marshmallow import ValidationError
from werkzeug.exceptions import HTTPException

from src.blueprints.blacklist import blacklists_blueprint
from src.blueprints.health_check import health_check_blueprint
from src.blueprints.email_registration import email_registration_blueprint
from src.database import db
from src.errors.errors import ApiError

env = os.getenv('FLASK_ENV', 'production')
if env == 'development':
    load_dotenv('.env.development')

DB_NAME = os.environ.get('RDS_DB_NAME')
DB_HOST = os.environ.get('RDS_HOSTNAME')
DB_PORT = os.environ.get('RDS_PORT')
DB_USER = os.environ.get('RDS_USERNAME')
DB_PASSWORD = os.environ.get('RDS_PASSWORD')
LOG_LEVEL = os.environ.get("LOG_LEVEL", logging.INFO)

app = Flask(__name__)
app.url_map.strict_slashes = False
app.logger.setLevel(LOG_LEVEL)
app.config["SQLALCHEMY_DATABASE_URI"] = (
    f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

db.init_app(app)

with app.app_context():
    db.create_all()

app.register_blueprint(health_check_blueprint)
app.register_blueprint(blacklists_blueprint)
app.register_blueprint(email_registration_blueprint)

@app.errorhandler(Exception)
def handle_exception(err):
    if isinstance(err, ApiError):
        response = {
            "msg": err.description,
            "version": os.environ["VERSION"]
        }
        return jsonify(response), err.code
    if isinstance(err, ValidationError):
        response = {
            "msg": err.messages_dict,
            "version": os.environ["VERSION"]
        }
        return jsonify(response), 400

    if isinstance(err, HTTPException):
        response = {
            "code": err.code,
            "name": err.name,
            "description": err.description,
            "version": os.environ.get("VERSION"),
        }
        return jsonify(response), err.code
