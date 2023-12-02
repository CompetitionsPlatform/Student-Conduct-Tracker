from App.models import Staff, Student, Admin
from App.database import db


def create_student(admin, studentID, firstname, lastname, password, contact, studentType, yearofStudy):
    """
    Create a new student with the provided information.

    Args:
        admin: The admin creating the student.
        studentID: The ID of the student.
        firstname: The first name of the student.
        lastname: The last name of the student.
        password: The password for the student.
        contact: The contact information for the student.
        studentType: The type of student.
        yearofStudy: The year of study for the student.

    Returns:
        Student: The newly created student object if successful, otherwise None.
    """
    new_student = admin.addStudent(studentID, firstname=firstname, lastname=lastname, password=password, contact=contact, studentType=studentType, yearofStudy=yearofStudy)
    if new_student:
        return new_student
    return None

def create_staff(admin, firstname, lastname, password, staffID, email, teachingExperience):
    """
    Create a new staff member with the provided information.

    Args:
        admin: The admin creating the staff member.
        firstname: The first name of the staff member.
        lastname: The last name of the staff member.
        password: The password for the staff member.
        staffID: The ID of the staff member.
        email: The email address of the staff member.
        teachingExperience: The teaching experience of the staff member.

    Returns:
        Staff: The newly created staff member object if successful, otherwise None.
    """
    new_staff = admin.addStaff(staffID, firstname=firstname, lastname=lastname, password=password, email=email, teachingExperience=teachingExperience)
    if new_staff:
        return new_staff
    return None

def create_user(firstname, lastname, password):
    """
    Create a new admin user with the provided information.

    Args:
        firstname: The first name of the admin user.
        lastname: The last name of the admin user.
        password: The password for the admin user.

    Returns:
        Admin: The newly created admin user object if successful, otherwise None.
    """
    new_admin = Admin(firstname=firstname, lastname=lastname, password=password)
    db.session.add(new_admin)
    db.session.commit()
    return new_admin

def get_staff(staffID):
    """
    Retrieve a staff member by their ID.

    Args:
        staffID: The ID of the staff member to retrieve.

    Returns:
        Staff: The staff member object if found, otherwise None.
    """
    return Staff.query.filter_by(ID=staffID).first()

def get_student(studentID):
    """Retrieve a student by their ID.

    Args:
        studentID: The ID of the student to retrieve.

    Returns:
        Student: The student object if found, otherwise None.
    """
    return Student.query.filter_by(ID=studentID).first()

def get_admin(adminID):
    """Retrieve an admin by their ID.

    Args:
        adminID: The ID of the admin to retrieve.

    Returns:
        Admin: The admin object if found, otherwise None.
    """
    return Admin.query.filter_by(ID=adminID).first()

def is_staff(staffID):
    """Check if a staff member with the given ID exists.

    Args:
        staffID: The ID of the staff member to check.

    Returns:
        bool: True if the staff member exists, False otherwise.
    """
    return db.session.query(Staff).get(staffID) is not None

def is_student(studentID):
    """
    Check if a student with the given ID exists.

    Args:
        studentID: The ID of the student to check.

    Returns:
        bool: True if the student exists, False otherwise.
    """
    return db.session.query(Student).get(studentID) is not None

def is_admin(AdminID):
    """
    Check if an admin with the given ID exists.

    Args:
        AdminID: The ID of the admin to check.

    Returns:
        bool: True if the admin exists, False otherwise.
    """
    return db.session.query(Admin).get(AdminID) is not None 

def get_all_users_json():
    """
    Get a JSON representation of all users.

    Returns:
        list: A list of JSON representations of users.
    """
    users = get_all_users()
    if not users:
        return []
    users = [user.to_json() for user in users]
    return users

def get_all_students_json():
    """
    Get a JSON representation of all students.

    Returns:
        list: A list of JSON representations of students.
    """
    students = get_all_students()
    if not students:
        return []
    students = [student.to_json() for student in students]
    return students

def get_all_staff_json():
    """
    Get a JSON representation of all staff members.

    Returns:
        list: A list of JSON representations of staff members.
    """
    staff_members = get_all_staff()
    if not staff_members:
        return []
    staff_members = [staff.to_json() for staff in staff_members]
    return staff_members

def get_all_users():
    """
    et all users in the system.

    Returns:
        list: A list containing all users (Admins, Staff, and Students).
    """
    return db.session.query(Admin).all() +  db.session.query(Staff).all() + db.session.query(Student).all()

def get_all_students():
    """
    Get all student records in the system.

    Returns:
        list: A list containing all student users.
    """
    return db.session.query(Student).all()

def get_all_staff():
    """
    Get all staff records in the system.

    Returns:
        list: A list containing all staff records.
    """
    return db.session.query(Staff).all()

def update_student(student, firstname, lastname, password, contact, studentType, yearofStudy):
    """
    Update a student's information.

    Args:
        student (Student): The student object to be updated.
        firstname (str): The new first name for the student.
        lastname (str): The new last name for the student.
        password (str): The new password for the student. If None, the password remains unchanged.
        contact (str): The new contact information for the student.
        studentType (str): The new student type for the student.
        yearofStudy (int): The new year of study for the student.

    Returns:
        Student: The updated student object.
    """
    student.firstname = firstname 
    student.lastname = lastname
    if password is not None:
      student.set_password(password)
    student.contact = contact
    student.studentType = studentType
    student.yearOfStudy = yearofStudy
    db.session.add(student)
    db.session.commit()
    return student