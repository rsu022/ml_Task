from flask import Flask, jsonify

app = Flask(__name__)

# Service function
def calculate_discount(price, discount):
    return price - (price * discount / 100)

# Controller using service
@app.route('/discount/<int:price>/<int:discount>')
def discount(price, discount):
    final_price = calculate_discount(price, discount)
    return jsonify({"final_price": final_price})

if __name__ == '__main__':
    app.run(debug=True)
