from flask import Blueprint

responses_bp = Blueprint("responses", __name__, url_prefix="/responses")


@responses_bp.route("/")
def get_all_responses():
    return "Get all responses"
