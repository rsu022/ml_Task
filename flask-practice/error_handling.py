from flask import Flask, jsonify

app = Flask(__name__)

# Custom 404 handler
@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Page not found"}), 404

# Exception example
@app.route('/divide/<int:a>/<int:b>')
def divide(a, b):
    try:
        result = a / b
        return jsonify({"result": result})
    except ZeroDivisionError:
        return jsonify({"error": "Cannot divide by zero"}), 400

if __name__ == '__main__':
    app.run(debug=True)
