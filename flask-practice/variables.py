from flask import Flask

app = Flask(__name__)

# Example variables
APP_NAME = "Flask Demo"
VERSION = "1.0.0"

@app.route('/info')
def info():
    return f"{APP_NAME} - Version {VERSION}"

if __name__ == '__main__':
    app.run(debug=True)
