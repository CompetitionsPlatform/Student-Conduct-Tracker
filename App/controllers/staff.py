from App.controllers.user import get_staff
from App.models import Staff, Student, Review, Karma
from App.database import db

def create_review(staffID, studentID, is_positive, comment):
    """
    Create a new review.

    Args:
        staffID (str): The ID of the staff member creating the review.
        studentID (str): The ID of the student being reviewed.
        is_positive (bool): True if the review is positive, False otherwise.
        comment (str): The comment associated with the review.

    Returns:
        Review or None: The created review if successful, or None on failure.
    """
    staff = get_staff(staffID)
    student = db.session.query(Student).get(studentID)
    
    if staff and student:
        review = staff.createReview(student,is_positive, comment)
        return review
    return None

def get_staff_reviews(staff_id):
    """
    Get reviews created by a specific staff member.

    Args:
        staff_id (str): The ID of the staff member.

    Returns:
        list: List of reviews created by the staff member.
    """
    staff = get_staff(staff_id)
    if staff:
        return staff.getReviewsByStaff(staff)

def search_students_searchTerm(staff, searchTerm):
    """
    Search for students based on a given search term.

    Args:
        staff: The staff member initiating the search.
        searchTerm (str): The term to search for (student ID, first name, or last name).

    Returns:
        list: List of students matching the search term.
    """
    students = staff.searchStudent(searchTerm)
    if students:
      return students
    return None
  
def get_student_rankings(staff):
    """
    Get the rankings of students based on their karma scores.

    Args:
        staff: The staff member retrieving the rankings.

    Returns:
        list: List of dictionaries containing student rankings.
    """
    return staff.getStudentRankings()