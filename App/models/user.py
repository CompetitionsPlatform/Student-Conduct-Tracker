from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import UserMixin
from App.database import db
from abc import ABC


class User(db.Model, UserMixin):
  __abstract__ = True

  firstname = db.Column(db.String(120), nullable=False)
  lastname = db.Column(db.String(120), nullable=False)
  password = db.Column(db.String(120), nullable=False)

  def __init__(self, firstname, lastname, password):
    """
    Initialize a new Admin instance.

    Args:
        firstname (str): The first name of the admin.
        lastname (str): The last name of the admin.
        password (str): The password for admin authentication.

    """
    self.firstname = firstname
    self.lastname = lastname
    self.set_password(password)

  def to_json(self):
    """
    Convert the Admin instance to a JSON-compatible dictionary.

    Returns:
        dict: A dictionary containing the admin's first and last names.

    """
    return {'firstname': self.firstname, 'lastname': self.lastname}

  def set_password(self, password):
    """
    Set the password for the Admin using a secure hash function.

    Args:
        password (str): The plaintext password to be hashed.
    """
    self.password = generate_password_hash(password, method='sha256')

  def check_password(self, password):
    """
    Check if the provided plaintext password matches the hashed password stored for the Admin.

    Args:
        password (str): The plaintext password to be checked.

    Returns:
        bool: True if the provided password matches the stored hashed password, False otherwise.
    """
    return check_password_hash(self.password, password)