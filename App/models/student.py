from App.database import db
from .user import User


class Student(User):
	__tablename__ = 'student'
	ID = db.Column(db.String(10), primary_key=True)
	contact = db.Column(db.String(30), nullable=False)
	studentType = db.Column(db.String(30))  #full-time, part-time or evening
	yearOfStudy = db.Column(db.Integer, nullable=False)
	reviews = db.relationship('Review', backref='student', lazy='joined')
	karmaID = db.Column(db.Integer, db.ForeignKey('karma.karmaID'))

	def __init__(self, studentID, firstname, lastname, password, contact, studentType, yearofStudy):
		"""
		Initialize a new Student instance.

		Args:
			studentID (str): The unique identifier for the student.
			firstname (str): The first name of the student.
			lastname (str): The last name of the student.
			password (str): The password for the student.
			contact (str): The contact information for the student.
			studentType (str): The type of student (e.g., undergraduate, graduate).
			yearofStudy (int): The current year of study for the student.

		Attributes:
			ID (str): The unique identifier for the student.
			contact (str): The contact information for the student.
			studentType (str): The type of student.
			yearOfStudy (int): The current year of study for the student.
			reviews (list): A list to store the reviews associated with the student.
		"""
		super().__init__(firstname, lastname, password)
		self.ID = studentID
		self.contact = contact
		self.studentType = studentType
		self.yearOfStudy = yearofStudy
		self.reviews = []
	
	def get_id(self):
		"""
		Get the unique identifier of the student.

    	Returns:
        		str: The unique identifier (ID) of the student.
		"""
		return self.ID

	def to_json(self):
		"""
		Convert the Student object to a JSON representation.

    	Returns:
        	dict: A dictionary containing the student's information in JSON format.
		"""
		karma = self.getKarma()
		return {
        "studentID": self.ID,
        "firstname": self.firstname,
        "lastname": self.lastname,
        "contact": self.contact,
        "studentType": self.studentType,
        "yearOfStudy": self.yearOfStudy,
        "reviews": [review.to_json() for review in self.reviews],
				"karmaScore": karma.score if karma else None,
        "karmaRank": karma.rank if karma else None,
    }

	def getKarma(self):
		"""
		Retrieve the Karma object associated with the student.

		Returns:
			Karma or None: The Karma object if associated, or None if not found.

		"""
		from .karma import Karma
		return Karma.query.get(self.karmaID)
