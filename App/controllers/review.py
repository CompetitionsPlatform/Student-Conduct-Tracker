from App.models import Review, Karma, Student
from App.database import db
from .student import search_student
from .karma import get_karma_by_id

def get_reviews():
    """
    Retrieve all reviews from the database.

    Returns:
        List[Review]: A list of Review objects.
    """
    return db.session.query(Review).all()

def get_reviews_for_student(studentID):
    """
    Retrieve all reviews associated with a specific student.

    Args:
        studentID (str): The ID of the student.

    Returns:
        List[Review]: A list of Review objects associated with the specified student.
    """
    return db.session.query(Review).filter_by(studentID=studentID).all()

def get_review(reviewID):
    """
    Retrieve a review by its ID.

    Args:
        reviewID (int): The ID of the review.

    Returns:
        Review or None: The Review object if found, or None if not found.
    """
    return Review.query.filter_by(ID=reviewID).first()

def get_reviews_by_staff(staffID):
    """
    Retrieve all reviews created by a staff member.

    Args:
        staffID (str): The ID of the staff member.

    Returns:
        List[Review]: A list of Review objects created by the specified staff member.
    """
    return db.session.query(Review).filter_by(reviewerID=staffID).all()

def edit_review(review, staff, isPositive, comment):
    """
    Edit a review if the staff member is the original reviewer.

    Args:
        review (Review): The review object to be edited.
        staff (Staff): The staff member attempting to edit the review.
        isPositive (bool): The new positive/negative status of the review.
        comment (str): The updated comment for the review.

    Returns:
        Review or None: The edited review if successful, else None.
    """
    if review.reviewer == staff:
        edited = review.editReview(staff, isPositive, comment)

        if edited:
            return review
        else:
            return None
    else:
        return None

def delete_review(review, staff):
    """
    Delete a review if the staff member is the original reviewer.

    Args:
        review (Review): The review object to be deleted.
        staff (Staff): The staff member attempting to delete the review.

    Returns:
        bool or None: True if the review is deleted successfully, else None.
    """
    if review.reviewer == staff:
        deleted = review.deleteReview(staff)
        return deleted
    return None

def handle_vote(review, staff, upvote):
    """
    Handle the upvote or downvote for a review.

    Args:
        review (Review): The review object.
        staff (Staff): The staff member casting the vote.
        upvote (bool): True for upvote, False for downvote.

    Returns:
        int or None: Number of upvotes if upvoted, number of downvotes if downvoted, or None on error.
    """
    try:
        if staff not in (review.staffUpvoters if upvote else review.staffDownvoters):
            if upvote:
                review.upvoteReview(staff)
            else:
                review.downvoteReview(staff)
            
            student = search_student(review.studentID)
            if student.karmaID is None:
                karma = Karma(score=0.0, rank=-99)
                db.session.add(karma)
                db.session.flush()
                student.karmaID = karma.karmaID

            student_karma = get_karma_by_id(student.karmaID)
            student_karma.calculateScore(student)
            student_karma.updateRank()

        return review.upvotes if upvote else review.downvotes
    
    except Exception as e:
        print (f'error handling vote {e}')
        db.session.rollback()
        return None

def downvoteReview(reviewID, staff):
    """
    Downvote a review.

    Args:
        reviewID (int): The ID of the review to downvote.
        staff (Staff): The staff member casting the downvote.

    Returns:
        int or None: Number of downvotes if downvoted, or None on error.
    """
    review = get_review(reviewID)

    if staff in review.staffDownvoters:  # If they downvoted the review already, return current votes
        return review.downvotes

    return handle_vote(review, staff, upvote=False)

def upvoteReview(reviewID, staff):
    """
    Upvote a review.

    Args:
        reviewID (int): The ID of the review to upvote.
        staff (Staff): The staff member casting the upvote.

    Returns:
        int or None: Number of upvotes if upvoted, or None on error.
    """
    review = get_review(reviewID)

    if staff in review.staffUpvoters:  # If they upvoted the review already, return current votes
        return review.upvotes

    return handle_vote(review, staff, upvote=True)