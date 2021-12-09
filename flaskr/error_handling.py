


from flask.wrappers import Response

import json

from flask import Blueprint

import json

bp = Blueprint('error_handling', __name__)

"""
userに関わるものは詳しく教えてあげる。
知られてはいけないエラーは教えてない。

"""

@bp.app_errorhandler(400)
def handle_400(err):
    error_message = {
        "message" : "Bad Request",
        "HTTP status " : 400
        }
    return Response(response = json.dumps(error_message), status = 400)


@bp.app_errorhandler(404)
def handle_404(err):
    error_message = {
        "message" : "Page Not Found",
        "HTTP status " : 404
        }
    return Response(response = json.dumps(error_message), status = 404)


@bp.app_errorhandler(405)
def handle_405(err):
    error_message = {
        "message" : "Method Not Allowed",
        "HTTP status " : 405
        }
    return Response(response = json.dumps(error_message), status = 405)


def response_error(message, status_code):
    error_message = {
        "message" : message,
        "HTTP status " : status_code
        }
    return Response(response = json.dumps(error_message), status = status_code)
        




































