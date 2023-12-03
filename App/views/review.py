from flask import Blueprint, jsonify, redirect, render_template, request, abort, url_for
from flask_jwt_extended import jwt_required, current_user as jwt_current_user
from flask_login import current_user
from App.controllers import Review, Staff
from App.controllers.user import get_staff
from App.controllers.student import search_student

from App.controllers.review import (
    get_reviews_by_staff,
    edit_review,
    delete_review,
    upvoteReview,
    downvoteReview,
    get_reviews,
    get_reviews_for_student, 
    get_review
)

# Create a Blueprint for Review views
review_views = Blueprint("review_views", __name__, template_folder='../templates')

# DONE Route to list all reviews (you can customize this route as needed)
@review_views.route('/reviews', methods=['GET'])
@jwt_required()
def list_reviews():
    reviews = get_reviews()
    return jsonify([review.to_json() for review in reviews]), 200

# Route to view a specific review and vote on it
@review_views.route('/reviews/<int:review_id>', methods=['GET'])
@jwt_required()
def view_review(review_id):
    review = get_review(review_id)
    if review:
        return jsonify(review.to_json())
    else: 
        return 'Review does not exist', 404

# Route to vote on a particular review
@review_views.route('/reviews/<int:review_id>', methods=['POST'])
@jwt_required()
def vote(review_id):
    if not jwt_current_user or not isinstance(jwt_current_user, Staff):
        return jsonify({"error": "You are not authorized to vote on this review"}), 401
    
    review = get_review(review_id)
    
    if review:
        data = request.json
        staff = get_staff(jwt_current_user.ID)
        
        if staff:
            if 'upvote' in data and isinstance(data['upvote'], bool):
                if data['upvote']:
                    current_votes = review.upvotes
                    new_votes = upvoteReview(review_id, staff)
                    message = 'Review Upvoted Successfully' if new_votes > current_votes else 'Review Already Upvoted'
                else:
                    current_votes = review.downvotes
                    new_votes = downvoteReview(review_id, staff)
                    message = 'Review Downvoted Successfully' if new_votes > current_votes else 'Review Already Downvoted'
                
                return jsonify(review.to_json(), message), 200
            else:
                return jsonify({"error": "Invalid request data. 'upvote' field must be a boolean"}), 400
        else:
            return jsonify({"error": "Staff does not exist"}), 404
    else:
        return jsonify({"error": "Review does not exist"}), 404

# Route to get reviews by student ID
@review_views.route("/students/<string:student_id>/reviews", methods=["GET"])
def get_reviews_of_student(student_id):
    if search_student(student_id):
        reviews = get_reviews_for_student(student_id)
        if reviews:
            return jsonify([review.to_json() for review in reviews]), 200
        else:
            return "No reviews found for the student", 404
    return "Student does not exist", 404

# Route to get reviews by staff ID
@review_views.route("/staff/<string:staff_id>/reviews", methods=["GET"])
def get_reviews_from_staff(staff_id):
    if get_staff(str(staff_id)):
        reviews = get_reviews_by_staff(staff_id)
        if reviews:
            return jsonify([review.to_json() for review in reviews]), 200
        else:
            return "No reviews found by the staff member", 404
    return "Staff does not exist", 404

# Route to edit a review
@review_views.route("/reviews/<int:review_id>", methods=["PUT"])
@jwt_required()
def review_edit(review_id):
    review = get_review(review_id)
    if not review:
      return "Review not found", 404
      
    if not jwt_current_user or not isinstance(jwt_current_user, Staff) or review.reviewerID != jwt_current_user.ID :
      return "You are not authorized to edit this review", 401

    staff = get_staff(jwt_current_user.ID)

    data = request.json

    if not data['comment']:
        return "Invalid request data", 400
    
    if data['isPositive'] not in (True, False):
        return jsonify({"message": f"invalid Positivity value  ({data['isPositive']}). Positive: true or false"}), 400

    updated= edit_review(review, staff, data['isPositive'], data['comment'])
    if updated: 
      return jsonify(review.to_json(), 'Review Edited'), 200
    else:
      return "Error updating review", 400

# Route to delete a review
@review_views.route("/reviews/<int:review_id>", methods=["DELETE"])
@jwt_required()
def review_delete(review_id):
    review = get_review(review_id)
    if not review:
      return "Review not found", 404

    if not jwt_current_user or not isinstance(jwt_current_user, Staff) or review.reviewerID != jwt_current_user.ID :
      return "You are not authorized to delete this review", 401

    staff = get_staff(jwt_current_user.ID)
   
    if delete_review(review, staff):
        return "Review deleted successfully", 200
    else:
        return "Issue deleting review", 400

