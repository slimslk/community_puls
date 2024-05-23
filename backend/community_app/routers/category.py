from flask import Blueprint, jsonify, Response, request, make_response
from pydantic import ValidationError

from community_app.models.question import Category
from community_app import db
from community_app.schemas.question import CategoryResponse, CategoryBase

category_bp = Blueprint("categories", __name__, url_prefix="/categories")


@category_bp.route("/", methods=["GET"])
def get_all_categories() -> Response:
    categories: list[Category, ...] = Category.query.all()

    categories_response = [
        CategoryResponse.from_orm(category).dict() for category in categories
    ]

    return make_response(jsonify(categories_response), 200)


@category_bp.route("/", methods=["POST"])
def add_category() -> Response:
    data = request.get_json()

    try:
        category_data = CategoryBase(**data)
    except ValidationError as err:
        return make_response(err.error, 400)

    category: Category = Category(
        name=category_data.name
    )

    db.session.add(category)
    db.session.commit()

    return make_response(jsonify(
        CategoryResponse.from_orm(category).dict()
    ), 201)


@category_bp.route("/<int:category_id>", methods=["PUT"])
def update_category_by_id(category_id: int):
    category: Category = Category.query.get(category_id)

    if category is None:
        return make_response(jsonify(
            {
                "message": "CATEGORY NOT FOUND"
            }
        ), 404)

    category_data = request.get_json()
    if not category_data or "name" not in category_data:
        return make_response(jsonify(
            {
                "message": "NO DATA PROVIDED"
            }
        ), 400)

    category.name = category_data["name"]
    db.session.commit()

    return make_response(jsonify(
        CategoryResponse.from_orm(category).dict()
    ), 200)


@category_bp.route("/<int:category_id>", methods=["DELETE"])
def delete_category_by_id(category_id: int):
    category: Category = Category.query.get(category_id)

    if category is None:
        return make_response(jsonify(
            {
                "message": "CATEGORY NOT FOUND"
            }
        ), 404)

    db.session.delete(category)
    db.session.commit()

    return make_response(jsonify(
        {
            "message": f"CATEGORY {category.id} - {category.name} DELETED SUCCESSFULLY"
        }
    ), 200)
