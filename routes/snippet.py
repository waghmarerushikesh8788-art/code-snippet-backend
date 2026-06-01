from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from extensions import mongo
from bson import ObjectId

snippet_bp = Blueprint("snippet", __name__)

def serialize_snippet(snippet):
    snippet["_id"] = str(snippet["_id"])
    return snippet

@snippet_bp.route("/create", methods=["POST"])
@jwt_required()
def create_snippet():
    data = request.get_json()
    user_id = get_jwt_identity()

    if not data:
        return jsonify({"message": "No data received"}), 400

    title = data.get("title", "").strip()
    code = data.get("code", "").strip()
    price = data.get("price", 0)

    if not title or not code:
        return jsonify({"message": "Title and code are required"}), 400

    try:
        price = int(price)
    except (ValueError, TypeError):
        return jsonify({"message": "Price must be a number"}), 400

    mongo.db.snippets.insert_one({
        "title": title,
        "code": code,
        "price": price,
        "owner": user_id
    })

    return jsonify({"message": "Snippet uploaded successfully"}), 201


@snippet_bp.route("/list", methods=["GET"])
def list_snippets():
    snippets = list(mongo.db.snippets.find())
    return jsonify([serialize_snippet(s) for s in snippets]), 200


@snippet_bp.route("/<snippet_id>", methods=["GET"])
def get_snippet(snippet_id):
    try:
        snippet = mongo.db.snippets.find_one({"_id": ObjectId(snippet_id)})
    except Exception:
        return jsonify({"message": "Invalid snippet ID"}), 400

    if not snippet:
        return jsonify({"message": "Snippet not found"}), 404

    return jsonify(serialize_snippet(snippet)), 200
