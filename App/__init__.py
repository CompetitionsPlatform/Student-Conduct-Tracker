from .models import *
from .views import *
from .controllers import *
from .main import *

def init():
    # Assuming db is your SQLAlchemy database object
    db.drop_all()
    db.create_all()

    admin = Admin('bob', 'boblast', 'bobpass')

    if admin:
        db.session.add(admin)
        db.session.commit()
    else:
        return jsonify({'error':'database error'}), 201

    log_staff = create_staff(admin, 'staff', 'stafflast', 'staffpass', '99', 'staff@schooling.com', 10)
    log_staff2 = create_staff(admin, 'nice', 'nicelast', 'nicepass', '69', 'staff2@schooling.com', 9)

    if log_staff and log_staff2:
        db.session.add(log_staff)
        db.session.add(log_staff2)
        db.session.commit()
    else:
        return jsonify({'error':'database error'}), 201

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

    log_stu = create_student(admin, '813', 'alice', 'alicelast', 'alicelast', contact, random.choice(['Full-Time', 'Part-Time', 'Evening']), str(random.randint(1, 8)))
    log_stu2 = create_student(admin, '666', 'trudy', 'trudylast', 'trudylast', contact, random.choice(['Full-Time', 'Part-Time', 'Evening']), str(random.randint(1, 8)))

    if log_stu and log_stu2:
        db.session.add(log_stu)
        db.session.add(log_stu2)
        db.session.commit()
    else:
        return jsonify({'error':'database error'}), 201

    return jsonify({'message':'database initialized'}), 201
