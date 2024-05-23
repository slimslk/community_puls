from flask import Blueprint, jsonify, Response, request, make_response
from pydantic import ValidationError

from community_app.models.question import Question, Category
from community_app import db
from community_app.schemas.question import QuestionCreate, QuestionResponse

questions_bp = Blueprint("questions", __name__, url_prefix="/questions")


@questions_bp.route("/", methods=["GET"])
def get_all_questions() -> Response:
    questions: list[Question, ...] = Question.query.all()

    results = [
        QuestionResponse(
            id=question.id,
            text=question.text,
            category_name=question.category.name
        ).dict() for question in questions
    ]

    response = make_response(jsonify(results), 200)

    response.headers["Custom-Header"] = "OUR CUSTOM HEADER"

    return response


@questions_bp.route("/", methods=["POST"])
def add_new_question() -> Response:
    data = request.get_json()

    if not data or "category_id" not in data:
        return make_response(jsonify(
            {
                "message": "NO DATA PROVIDED"
            }
        ), 400)

    category_id = data["category_id"]
    category = Category.query.get(category_id)

    if category is None:
        return make_response(jsonify(
            {
                "message": f"The category with this ID {category_id} does not exist."
            }
        ), 400)

    try:
        question_data = QuestionCreate(**data)
    except ValidationError as err:
        return make_response(jsonify(err.errors()), 400)

    question: Question = Question(
        text=question_data.text,
        category_id=question_data.category_id
    )

    db.session.add(question)
    db.session.commit()

    return make_response(
        jsonify(QuestionResponse(
            id=question.id,
            text=question.text,
            category_name=question.category.name
        ).dict()), 201
    )


@questions_bp.route("/<int:question_id>")
def get_question_by_id(question_id: int) -> Response:
    question: Question = Question.query.get(question_id)

    if not question:
        return make_response(jsonify(
            {
                "message": "NOT FOUND"
            }
        ), 404)

    question_data = {
        "id": question.id,
        "text": question.text,
        "created_at": question.created_at
    }

    return make_response(jsonify(question_data), 200)


@questions_bp.route("/<int:question_id>", methods=["PUT"])
def update_question_by_id(question_id: int) -> Response:
    question: Question = Question.query.get(question_id)

    if not question:
        return make_response(jsonify(
            {
                "message": f"QUESTION {question_id} NOT FOUND"
            }
            ), 404
        )

    request_data: dict[str] = request.get_json()

    if not request_data or ("text" not in request_data and "category_id" not in request_data):
        return make_response(jsonify(
            {
                "message": "NO DATA PROVIDED"
            }
        ), 404)

    if request_data.get("text") is not None:
        question.text = request_data["text"]
    if request_data.get("category_id") is not None:

        category = Category.query.get(request_data["category_id"])
        if category is None:
            return make_response(jsonify(
                {
                    "message": f"The category with this ID {request_data["category_id"]} does not exist."
                }
            ), 400)

    db.session.commit()

    return make_response(jsonify(
        {
            "message": f"Question {question.id} updated successfully",
            "new_text": question.text,
            "category_name": question.category.name
        }
    ), 200)


@questions_bp.route("/<int:question_id>", methods=["DELETE"])
def delete_question_by_id(question_id: int) -> Response:
    question: Question = Question.query.get(question_id)

    if not question:
        return make_response(jsonify(
            {
                "message": f"QUESTION {question_id} NOT FOUND"
            }
            ), 404
        )

    db.session.delete(question)
    db.session.commit()

    return make_response(jsonify(
        {
            "message": "QUESTION DELETED SUCCESSFULLY"
        }
    ), 200)
