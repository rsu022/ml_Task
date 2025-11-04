from app.controllers.student_controller import student_blueprint

def register_blueprints(app):
    app.register_blueprint(student_blueprint, url_prefix="/api")
