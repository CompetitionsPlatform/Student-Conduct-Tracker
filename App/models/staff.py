from App.database import db
from .user import User
from .student import Student
from .karma import Karma
from .review import Review


class Staff(User):
  __tablename__ = 'staff'
  ID = db.Column(db.String(10), primary_key=True)
  email = db.Column(db.String(120), nullable=False)
  teachingExperience = db.Column(db.Integer, nullable=False)

  def __init__(self, staffID, firstname, lastname, password, email,
               teachingExperience):
    """
    Initialize a Staff instance.

    Args:
        staffID (str): The unique identifier for the staff.
        firstname (str): The first name of the staff.
        lastname (str): The last name of the staff.
        password (str): The password for the staff.
        email (str): The email address of the staff.
        teachingExperience (int): The number of years of teaching experience.
    """
    super().__init__(firstname, lastname, password)
    self.ID = staffID
    self.email = email
    self.teachingExperience = teachingExperience

  def get_id(self):
    """
    Get the unique identifier of the Staff.

    Returns:
        str: The staff ID.
    """
    return self.ID

  def to_json(self):
    """
    Convert Staff object to a JSON-compatible dictionary.

    Returns:
        dict: A dictionary containing staff information.
    """
    return {
        "staffID": self.ID,
        "firstname": self.firstname,
        "lastname": self.lastname,
        "email": self.email,
        "teachingExperience": self.teachingExperience
    }

  def getReviewsByStaff(self, staff):
    """
    Get reviews created by a staff member.

    Args:
        staff (Staff): The staff member.

    Returns:
        list: List of dictionaries representing reviews created by the staff.
    """
    staff_reviews = staff.reviews_created
    return [review.to_json() for review in staff_reviews]

  def createReview(self, student, isPositive, comment):
    """
    Create a review by a staff member for a student.

    Args:
        student (Student): The student for whom the review is created.
        isPositive (bool): Indicates whether the review is positive or not.
        comment (str): The comment provided in the review.

    Returns:
        dict: Dictionary representing the created review.
    """
    review = Review(self, student, isPositive, comment)
    student.reviews.append(review)  #add review to the student
    
    return self.dataCommit(review)

  def searchStudent(self, searchTerm):
    """
    Search for students by ID, first name, or last name.

    Args:
        searchTerm (str): The search term (ID, first name, or last name).

    Returns:
        list: List of dictionaries representing matching students.
    """
    # Query the Student model for a student by ID or first name, or last name
    students = db.session.query(Student).filter(
        (Student.ID == searchTerm)
        |  #studentID must be exact match (string)
        (Student.firstname.ilike(f"%{searchTerm}%"))
        |  # Search by firstname or lastname - case-insensitive
        (Student.lastname.ilike(f"%{searchTerm}%"))).all()

    if students:
      # If matching students are found, return their json representations in a list
      return [student.to_json() for student in students]
    else:
      # If no matching students are found, return an empty list
      return []

  def getStudentRankings(self):
    """
    Get the rankings of students based on their karma scores.

    Returns:
        list: List of dictionaries representing student rankings.
    """
    students = db.session.query(Student, Karma)\
                .join(Karma, Student.karmaID == Karma.karmaID)\
                .order_by(Karma.rank.asc())\
                .all()

    if students:
      # If students with rankings are found, return a list of their JSON representations
      student_rankings = [{
          "studentID": student.Student.ID,
          "firstname": student.Student.firstname,
          "lastname": student.Student.lastname,
          "karmaScore": student.Karma.score,
          "karmaRank": student.Karma.rank
      } for student in students]
      return student_rankings
    else:
      # If no students with rankings are found, return an empty list
      return []

  @staticmethod
  def dataCommit(entity):
    """
    Commit the provided entity to the database.

    Args:
        entity: The entity (e.g., Review, Student, Karma) to be committed to the database.

    Returns:
        entity: The committed entity if successful, None otherwise.
    """
    try:
      db.session.add(entity)
      db.session.commit()
      return entity
    except Exception as e:
      db.session.rollback()
      print(f'Error: {e}')
      return None