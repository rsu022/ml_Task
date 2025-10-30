from flask import Flask, jsonify

app = Flask(__name__)

# JSON response
@app.route('/product')
def product():
    product_data = {
        "id": 101,
        "name": "Laptop",
        "price": 75000
    }
    return jsonify(product_data)  # jsonify handles serialization

if __name__ == '__main__':
    app.run(debug=True)
