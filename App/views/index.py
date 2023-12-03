import random
from flask import Blueprint, render_template, jsonify, session
from App.models import db
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token
from App.controllers import create_user, create_staff, create_student, jwt_authenticate, jwt_authenticate_admin, login 
import randomname

from App.models.admin import Admin

index_views = Blueprint('index_views', __name__, template_folder='../templates')

# Define a route for the index view
@index_views.route('/', methods=['GET'])
def index_page():
    return render_template('index.html')

def generate_random_contact_number():
    return f"0000-{random.randint(100, 999)}-{random.randint(1000, 9999)}"


@index_views.route('/init', methods=['GET'])
def init():
    # Assuming db is your SQLAlchemy database object
    db.drop_all()
    db.create_all()

    admin = create_user('bob', 'boblast', 'bobpass')

    for ID in range(2, 50):
        staff = create_staff(admin,
                             randomname.get_name(),
                             randomname.get_name(),
                             randomname.get_name(),
                             str(ID),
                             randomname.get_name() + '@schooling.com',
                             str(random.randint(1, 15))
                             )
        db.session.add(staff)

    db.session.commit()

    for ID in range(50, 150):
        contact = generate_random_contact_number()
        student = create_student(admin, str(ID),
                                 randomname.get_name(),
                                 randomname.get_name(),
                                 randomname.get_name(),
                                 contact,
                                 random.choice(['Full-Time', 'Part-Time', 'Evening']),
                                 str(random.randint(1, 8))
                                 )
        db.session.add(student)

    db.session.commit()

    # Log in the admin user
    user = login(admin.ID, 'bobpass')

    if user:
        # Log in the user
        session['logged_in'] = True

        # Create a JWT token
        token = create_access_token(identity=user.ID)

        # Return the token as part of the response
        response = {'message': 'Admin user logged in', 'jwt_token': token}
    else:
        response = {'message': 'Admin login failed'}

    # Optionally, print the response or return it
    return jsonify(response), 201

    #return jsonify({'message': 'Database initialized'},{f'token':'{token}'}), 201