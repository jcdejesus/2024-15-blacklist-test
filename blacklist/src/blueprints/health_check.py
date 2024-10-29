from flask import Blueprint

health_check_blueprint = Blueprint('health_check', __name__, url_prefix='/blacklists')


@health_check_blueprint.route('/ping', methods=['GET'])
def ping_pong():
    return "pong", 200
