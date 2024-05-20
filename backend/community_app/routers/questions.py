from flask import Blueprint

questions_bp = Blueprint("questions", __name__, url_prefix="/questions")


@questions_bp.route("/")
def get_all_questions():
    return "Get all questions"


@questions_bp.route("/add", methods=["POST"])
def add_new_question():
    return "New question added"


@questions_bp.route("/questions/<int:question_id>")
def get_question_by_id(question_id: int):
    return f"Getting question by id - {question_id}"


@questions_bp.route("/questions/<int:question_id>", methods=["PUT"])
def update_question_by_id(question_id: int):
    return f"Updated question by ID: {question_id}"


@questions_bp.route("/questions/<int:question_id>", methods=["DELETE"])
def delete_question_by_id(question_id: int):
    return f"Deleted question by ID: {question_id}"
