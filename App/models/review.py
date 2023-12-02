from App.database import db
from .student import Student
from datetime import datetime
from .karma import Karma

# Define the association table for staff upvotes on reviews
review_staff_upvoters = db.Table(
    'review_staff_upvoters',
    db.Column('reviewID', db.Integer, db.ForeignKey('review.ID')),
    db.Column('staffID', db.String(10), db.ForeignKey('staff.ID')),
)

review_staff_downvoters = db.Table(
    'review_staff_downvoters',
    db.Column('reviewID', db.Integer, db.ForeignKey('review.ID')),
    db.Column('staffID', db.String(10), db.ForeignKey('staff.ID')),
)


class Review(db.Model):
  __tablename__ = 'review'
  ID = db.Column(db.Integer, primary_key=True)
  reviewerID = db.Column(db.String(10), db.ForeignKey('staff.ID'))  #each review has 1 creator
  reviewer = db.relationship('Staff', backref=db.backref('reviews_created', lazy='joined'), foreign_keys=[reviewerID]) #create reverse relationship from Staff back to Review to access reviews created by a specific staff member
  studentID = db.Column(db.String(10), db.ForeignKey('student.ID'))
  staffUpvoters = db.relationship('Staff', secondary=review_staff_upvoters, backref=db.backref('reviews_upvoted', lazy='joined'))  #for staff who have voted on the review
  staffDownvoters = db.relationship('Staff', secondary=review_staff_downvoters, backref=db.backref('reviews_downvoted', lazy='joined'))  #for staff who have voted on the review
  upvotes = db.Column(db.Integer, nullable=False)
  downvotes = db.Column(db.Integer, nullable=False)
  isPositive = db.Column(db.Boolean, nullable=False)
  created = db.Column(db.DateTime, default=datetime.utcnow)
  comment = db.Column(db.String(400), nullable=False)

  subscribers = db.relationship('Karma', backref='review', lazy=True)

  def __init__(self, reviewer, student, isPositive, comment):
    """
    Initialize a new Review object.

    Args:
        reviewer (Staff): The staff member who created the review.
        student (Student): The student who the review is about.
        isPositive (bool): Indicates whether the review is positive or not.
        comment (str): The comment or description provided in the review.
    """
    self.reviewerID = reviewer.ID
    self.reviewer = reviewer
    self.studentID = student.ID
    self.isPositive = isPositive
    self.comment = comment
    self.upvotes = 0
    self.downvotes = 0
    self.created = datetime.now()

  def get_id(self):
    """
    Get the ID of the Review.

    Returns:
        int: The ID of the Review.
    """
    return self.ID

  def editReview(self, staff, isPositive, comment):
    """
    Edit the Review details.

    Args:
        staff (Staff): The staff member attempting to edit the review.
        isPositive (bool): The updated positivity status of the review.
        comment (str): The updated comment for the review.

    Returns:
        bool: True if the review is successfully edited, None otherwise.
    """
    if self.reviewer == staff:
      self.isPositive = isPositive
      self.comment = comment
      db.session.add(self)
      db.session.commit()
      return True
    return None

  def deleteReview(self, staff):
    """
    Delete the review if the staff member is the reviewer.

    Args:
        staff (Staff): The staff member attempting to delete the review.

    Returns:
        bool: True if the review is successfully deleted, None otherwise.
    """
    if self.reviewer == staff:
      db.session.delete(self)
      self.removeSubscriber()
      self.notifySubscriber()
      db.session.commit()
      return True
    return None

  def upvoteReview(self, staff):
    """
    Delete the review if the staff member is the reviewer.

    Args:
        staff (Staff): The staff member attempting to delete the review.

    Returns:
        bool: True if the review is successfully deleted, None otherwise.
    """
    if staff in self.staffUpvoters:
      return self.upvotes
    
    self.upvotes += 1
    self.staffUpvoters.append(staff)
    
    if staff in self.staffDownvoters:
      self.downvotes -= 1
      self.staffDownvoters.remove(staff)
    
    db.session.add(self)
    db.session.commit()
    
    self.notifySubscriber()
    
    return self.upvotes

  def downvoteReview(self, staff):
    """
    Downvote the review by a staff member.

    Args:
        staff (Staff): The staff member downvoting the review.

    Returns:
        int: The updated number of downvotes.
    """
    if staff in self.staffDownvoters:
      return self.downvotes

    self.downvotes += 1
    self.staffDownvoters.append(staff)

    if staff in self.staffUpvoters:
      self.upvotes -= 1
      self.staffUpvoters.remove(staff)

    db.session.add(self)
    db.session.commit()

    self.notifySubscriber()

    return self.downvotes
  
  def updateKarma(self):
    """
    Update the karma for the associated student.
    """
    student = Student.query.get(self.studentID)
    
    if student.karmaID is None:
      karma = Karma(score=0.0, rank=-99)
      db.session.add(karma)
      db.session.flush()
      student.karmaID = karma.karmaID

      student_karma = Karma.query.get(student.karmaID)
      student_karma.calculateScore(student)
      student_karma.updateRank()
      try:
        db.session.commit()
      except Exception as e:
        print (f'error updating karma {e}')
        db.session.rollback()
  
  def to_json(self):
    """
    Convert the review instance to a JSON-formatted dictionary.
    """
    return {
        "reviewID": self.ID,
        "reviewer": self.reviewer.firstname + " " + self.reviewer.lastname,
        "studentID": self.student.ID,
        "studentName": self.student.firstname + " " + self.student.lastname,
        "created":
        self.created.strftime("%d-%m-%Y %H:%M"),  #format the date/time
        "isPositive": self.isPositive,
        "upvotes": self.upvotes,
        "downvotes": self.downvotes,
        "comment": self.comment
    }

  def addSubscriber(self, subscriber):
    if subscriber not in self.subscribers:
      self.subscribers.append(subscriber)

  def removeSubscriber(self):
    for subscriber in self.subscribers:
      if subscriber in self.subscribers:
        self.subscribers.remove(subscriber)

  def notifySubscriber(self):
    for subscriber in self.subscribers:
      subscriber.update()