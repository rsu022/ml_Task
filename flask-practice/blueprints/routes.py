from flask import Blueprint, jsonify, request

bp = Blueprint('bp', __name__)

@bp.route('/post-name', methods=['POST'])
def post_name():
    data = request.json
    name = data.get("name", "Guest")
    return jsonify({"message": f"Hello, {name}!"})
