from flask import Flask, jsonify

app = Flask(__name__)

# Controller function
def get_users_controller():
    users = [
        {"id": 1, "name": "RSU"},
        {"id": 2, "name": "Alex"}
    ]
    return jsonify(users)

# Route using controller
@app.route('/users')
def users():
    return get_users_controller()

if __name__ == '__main__':
    app.run(debug=True)
