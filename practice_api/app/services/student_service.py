from app.database import db
from app.models.student_model import Student  # import model here

def get_all_students():
    students = Student.query.all()
    return [{"id": s.id, "name": s.name, "semester": s.semester} for s in students]

def get_student_by_id(student_id):
    student = Student.query.get(student_id)
    if student:
        return {"id": student.id, "name": student.name, "semester": student.semester}
    return {"error": "Student not found"}

def add_student(name, semester):
    # Check if student already exists
    existing = Student.query.filter_by(name=name).first()
    if existing:
        return {"message": f"Student '{name}' already exists"}  # skip duplicate
    student = Student(name=name, semester=semester)
    db.session.add(student)
    db.session.commit()
    return {"message": f"Student '{name}' added successfully"}


def update_student(student_id, name, semester):
    # Check if name already exists for another student
    existing = Student.query.filter(Student.name == name, Student.id != student_id).first()
    if existing:
        return {"error": f"Name '{name}' already exists for another student"}

    student = Student.query.get(student_id)
    if not student:
        return {"error": "Student not found"}
    student.name = name
    student.semester = semester
    db.session.commit()
    return {"message": "Student updated successfully"}


def delete_student(student_id):
    student = Student.query.get(student_id)
    if not student:
        return {"error": "Student not found"}
    db.session.delete(student)
    db.session.commit()
    return {"message": "Student deleted successfully"}
