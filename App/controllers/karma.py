from App.models import Karma, Student
from App.database import db

def get_karma_by_id(karma_id):
    """
    Retrieve a Karma instance by its ID.

    Args:
        karma_id (int): The ID of the Karma instance to be retrieved.

    Returns:
        Karma or None: The Karma instance if found, or None if not found.
    """
    return db.session.query(Karma).get(karma_id)

def calculate_student_karma(student):
    """
    Calculate the karma for a given student.

    Args:
        student (Student): The Student instance for which to calculate karma.
    """
    try:
        if student.karmaID is not None:
            karma = db.session.query(Karma).get(student.karmaID)
        else:
            karma = Karma(score=0.0, rank=-99)
            db.session.add(karma)
            db.session.flush()
            student.karmaID = karma.karmaID

        karma.calculateScore(student)
    
    except Exception as e:
        print('error calculating student karma')
        db.session.rollback()

def update_student_karma_rankings():
    """
    Update the karma rankings for all students based on their karma scores.
    """
    students_with_karma = db.session.query(Student, Karma)\
        .join(Karma, Student.karmaID == Karma.karmaID)\
        .order_by(db.desc(Karma.score))\
        .all()

    rank = 1
    prev_score = None

    for student, karma in students_with_karma:
        if prev_score is None:
            prev_score = karma.score
            karma.rank = rank
        elif prev_score == karma.score:
            karma.rank = rank
        else:
            rank += 1
            karma.rank = rank
            prev_score = karma.score

        student.karmaID = karma.karmaID
    
    try:
        db.session.commit()
    except Exception as e:
        print('error calculating karma')
        db.session.rollback()