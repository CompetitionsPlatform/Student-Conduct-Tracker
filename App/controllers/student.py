from App.models import Student
from App.database import db


def search_student(studentID):
    """
    Search for a student by their ID.

    Args:
        studentID: The ID of the student to search for.

    Returns:
        Student: The student object if found, otherwise None.
    """
    student = db.session.query(Student).get(studentID)
    if student:
        return student
    return None
