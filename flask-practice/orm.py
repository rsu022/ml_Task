from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text

# Initialize the Flask application
app = Flask(__name__)

# Configure the database URI for SQLite
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'

# Disable modification tracking for performance
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize SQLAlchemy for ORM functionality
db = SQLAlchemy(app)

# User model define garcha
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)

# Route to add a default user using GET for quick testing
@app.route('/add', methods=['GET'])
def add_user():
    user = User(name="Ariana Grande")
    db.session.add(user)
    db.session.commit()
    return "Inserted using ORM"

# Route to fetch all users using a raw SQL query
@app.route('/sql-users', methods=['GET'])
def get_users_sql():
    result = db.session.execute(text("SELECT * FROM user"))
    data = [{"id": row.id, "name": row.name} for row in result]
    return jsonify(data)

# Route to add a user dynamically using POST and JSON input
@app.route('/add-user', methods=['POST'])
def add_user_post():
    data = request.get_json()
    name = data.get("name")
    if not name:
        return jsonify({"error": "name is required"}), 400
    new_user = User(name=name)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({
        "message": "User added successfully",
        "user": {"id": new_user.id, "name": new_user.name}
    })

# Route to fetch all users from the database and return as JSON
@app.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    data = [{"id": u.id, "name": u.name} for u in users]
    return jsonify(data)


# Main entry point to create tables and run the Flask server
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
