import os

from flask import Blueprint, request, jsonify

from src.commands.email_banned import EmailBanned

blacklists_blueprint = Blueprint('blacklists', __name__, url_prefix='/blacklists')


@blacklists_blueprint.route('/<email>', methods=['GET'])
def get_status_email(email):
    token = request.headers.get('Authorization')
    if token != f"Bearer {os.environ.get('STATIC_TOKEN')}":
        return jsonify({"msg": "Unauthorized"}), 401

    record = EmailBanned(email).execute()
    return jsonify(record), 200
