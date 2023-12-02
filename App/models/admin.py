from App.database import db
from .student import Student
from .staff import Staff
from .user import User

class Admin(User):
	__tablename__ = 'admin'
	ID = db.Column(db.String, primary_key=True)

	def __init__(self, firstname, lastname, password):
		"""
		Init a new instance of the class Admin
		
		Args:
			firstname(str): the first name of the admin
			lastname(str): the last name of the admin
			firstname(str): the password of the user
		Returns:
			None			
		"""
		super().__init__(firstname, lastname, password)
		self.ID = "A" + str(Admin.query.count() + 1)

	def get_id(self):
		"""
		Get the unique identifier of the instance.

		Returns:
			str: The unique identifier of the instance.

		"""
		return self.ID

	def addStudent(self, id, firstname, lastname, password, contact, studentType, yearofStudy):
		"""
		Create a new student instance and add it to the database.

		Args:
			id (str): The unique identifier for the student.
			firstname (str): The first name of the student.
			lastname (str): The last name of the student.
			password (str): The password for the student.
			contact (str): The contact information of the student.
			studentType (str): The type of student.
			yearofStudy (int): The year of study for the student.

		Returns:
			Student or None: The created student instance if successful, otherwise None.
		"""

		newStudent= Student(id, firstname, lastname, password, contact, studentType, yearofStudy)
		return self.dataCommit(newStudent)

	# add staff to the database
	def addStaff(self, id, firstname, lastname, password, email, teachingExperience):
		"""
		Create a new staff member instance and add it to the database.

		Args:
			id (str): The unique identifier for the staff member.
			firstname (str): The first name of the staff member.
			lastname (str): The last name of the staff member.
			password (str): The password for the staff member.
			email (str): The email address of the staff member.
			teachingExperience (int): The years of teaching experience for the staff member.

		Returns:
			Staff or None: The created staff member instance if successful, otherwise None.
		"""
		newStaff= Staff(id, firstname, lastname, password, email, teachingExperience)
		
		return self.dataCommit(newStaff)

	def updateStudent(self, studentID, field_to_update, new_value):
		"""
		Update a specific field for a student in the database.

		Args:
			studentID (str): The unique identifier for the student.
			field_to_update (str): The field to update for the student.
			new_value: The new value to set for the specified field.

		Returns:
			Union[bool, str]: True if the update is successful, an error message if unsuccessful.
    	"""
		allowed_fields = ["ID", "contact", "firstname", "lastname", "password", "studenttype", "yearofstudy"]# List of fields that can be updated for a student record
		
		input_field = self.normalizeField(field_to_update)
		
		student = self.getStudentByID(studentID)
		if student is None:
			return "Student not found"

		# Check if the specified field exists in the Student model, change column names on model to lowercase so that it could be compared to the normalized input
		found_field = None
		for field in Student.__table__.columns.keys():
			if field.lower() == input_field:
				found_field = field
				break

		if found_field is None:
			return f"Field '{field_to_update}' does not exist for Student"

		# Check if the specified field is in the list of editable fields
		if input_field not in allowed_fields:
			return f"Field '{field_to_update}' cannot be updated for Student"

		# Update the specified field with the new value
		setattr(student, found_field, new_value)

		# Commit to save the changes
		save = self.dataCommit(student)

		if save:
			return True
		return False
	
	def to_json(self):
		"""
		Convert Admin object to a JSON representation.

    	Returns:
        	dict: A dictionary containing the JSON representation of the Admin object.
		"""
		return {
	        "adminID": self.ID,
    	    "firstname": self.firstname,
        	"lastname": self.lastname,
    	}
	
	@staticmethod
	def dataCommit(entity):
		"""
		Commit an entity to the database.

		Args:
			entity: The entity (e.g., Admin, Student, Staff) to be committed to the database.

		Returns:
			object or None: The committed entity if successful, otherwise None.

		"""
		try:
			db.session.add(entity)
			db.session.commit()
			return entity
		except Exception as e:
			db.session.rollback()
			print(f'Error: {e}')
			return None
	
	@staticmethod
	def normalizeField(field_to_update):
		"""
		Normalize a field name by converting it to lowercase and removing spaces, underscores, and dashes.

		Args:
			field_to_update (str): The field name to be normalized.

		Returns:
			str: The normalized field name.
		"""
		return field_to_update.lower().replace('-', '').replace('_', '').replace(' ', '')
	
	def getStudentByID(id):
		"""
		Retrieve a student record based on the given student ID.

		Args:
			id (str): The ID of the student to retrieve.

		Returns:
			Student or None: The Student object if found, otherwise None.
		"""
		student = Student.query.filter_by(ID=id).first() # Retrieve the student record based on student id
		if student:
			return student
		return None