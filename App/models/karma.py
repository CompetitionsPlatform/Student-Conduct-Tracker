from App.database import db
from .student import Student

class Karma(db.Model):
  __tablename__ = "karma"
  karmaID = db.Column(db.Integer, primary_key=True)
  score = db.Column(db.Float, nullable=False, default=0.0)
  rank = db.Column(db.Integer, nullable=False, default=-99)
  review_id = db.Column(db.Integer, db.ForeignKey('review.ID'), nullable=True, unique=True)

  def __init__(self, score=0.0, rank=-99):
    """
    Initialize a new Karma object with the given score and rank.

    Args:
        score (float, optional): The initial score of the Karma object. Defaults to 0.0.
        rank (int, optional): The initial rank of the Karma object. Defaults to -99.
    """
    self.score = score
    self.rank = rank

  def to_json(self):
    """
    Convert the Karma object to a JSON-compatible dictionary.

    Returns:
        dict: A dictionary representing the Karma object with keys for 'karmaID', 'score', and 'rank'.
    """
    return {"karmaID": self.karmaID, "score": self.score, "rank": self.rank}

  def calculateScore(self, student):
    """
    Calculate the Karma score based on the student's reviews.

    Args:
        student (Student): The Student object for which the Karma score is calculated.

    Returns:
        float: The calculated Karma score.
    """
    goodKarma = 0
    badKarma = 0

    # Iterate through reviews associated with the student
    for review in student.reviews:
      if review.isPositive == True:  #if review is positive then upvotes on the review contributes to good karma
        goodKarma += review.upvotes
        badKarma += review.downvotes
      else:  #if review is not positive then upvotes on the review contributes to bad karma
        badKarma += review.upvotes
        goodKarma += review.downvotes

    # Calculate the karma score
    self.score = goodKarma - badKarma

    # connect the karma record to the student
    student.karmaID = self.karmaID

    # Commit the changes to the database
    try:
      db.session.add(self)
      db.session.commit()
      return self.score
    except Exception as e:
      print(f'error calculating karma score {e}')
      db.session.rollback()
      return None

  @classmethod
  def updateRank(cls):
    """
    Update the rank of students based on their Karma scores.
    """
    # Calculate the rank of students based on their karma score

    # Query all students with karma scores in descending order
    studentsOrdered = db.session.query(Student, Karma)\
               .join(Karma, Student.karmaID == Karma.karmaID)\
               .order_by(db.desc(Karma.score))\
               .all()

    rank = 1
    prev_score = None

    #assign ranks to student with the highest karma at the top
    for student, karma in studentsOrdered:
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

  # Commit the changes to the database
    try:
      db.session.commit()
    except Exception as e:
      print(f'error updating karma rank {e}')
      db.session.rollback()

  @classmethod
  def getScore(cls, karmaID):
    """
    Retrieve the Karma score by Karma ID.

    Args:
        karmaID (int): The ID of the Karma record.

    Returns:
        float: The Karma score.
    """
    # Retrieve the karma score by karma id
    karma = cls.query.filter_by(karmaID=karmaID).first()
    if karma:
      return karma.score
    return None

  def update(self):
    self.calculateScore()
    self.updateRank()