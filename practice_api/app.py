from app import create_app

app = create_app()  # create Flask app instance

if __name__ == "__main__":
    app.run(debug=True)  # run server locally in debug mode
