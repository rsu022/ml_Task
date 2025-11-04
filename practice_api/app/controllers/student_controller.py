from flask import Blueprint, jsonify, request
from app.services.student_service import (
    get_all_students,
    get_student_by_id,
    add_student,
    update_student,
    delete_student,
)
from app.models.student_model import Student  # import model

student_blueprint = Blueprint("student_blueprint", __name__)

# GET all students
@student_blueprint.route("/students", methods=["GET"])
def list_students():
    return jsonify(get_all_students()), 200

# GET single student by ID
@student_blueprint.route("/students/<int:student_id>", methods=["GET"])
def get_student(student_id):
    return jsonify(get_student_by_id(student_id)), 200

# POST new student
@student_blueprint.route("/students", methods=["POST"])
def add_students_api():
    data = request.json
    if not isinstance(data, list):
        return jsonify(add_student(data.get("name"), data.get("semester"))), 201

    results = []
    for student_data in data:
        results.append(add_student(student_data.get("name"), student_data.get("semester")))
    return jsonify(results), 201

# PUT update student by ID
@student_blueprint.route("/students/<int:student_id>", methods=["PUT"])
def update_student_api(student_id):
    data = request.json
    return jsonify(update_student(student_id, data.get("name"), data.get("semester"))), 200

# DELETE student by ID
@student_blueprint.route("/students/<int:student_id>", methods=["DELETE"])
def delete_student_api(student_id):
    return jsonify(delete_student(student_id)), 200
