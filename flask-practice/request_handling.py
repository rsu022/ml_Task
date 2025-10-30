from flask import Flask, request, jsonify

app = Flask(__name__)

# GET request
@app.route('/get-name', methods=['GET'])
def get_name():
    name = request.args.get('name', 'Reshu')  # URL param ?name=RSU
    return f"Hello, {name}!"

# POST request
@app.route('/post-name', methods=['GET', 'POST'])
def post_name():
    if request.method == 'POST':
        data = request.json
        name = data.get('name', 'Guest')
        return jsonify({"message": f"Hello, {name}!"})
    else:
        return "Send a POST request with JSON"

if __name__ == '__main__':
    app.run(debug=True)
