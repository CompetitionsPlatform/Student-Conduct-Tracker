from App.database import db
from .subscriber import *


class Publisher(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    subscribers = db.relationship('Subscriber', backref='publisher', lazy=True)

    def __init__(self, name):
      self.name = name

    def subscribe(self, subscriber):
      self.subscribers.append(subscriber)

    def unsubscribe(self, subscriber):
       self.subscribers.remove(subscriber)

    def notify_subscribers(self):
        for subscriber in self.subscribers:
            subscriber.update()

class State(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  message = db.Column(db.String(50), nullable=False)
  subscriber_id = db.Column(db.Integer, db.ForeignKey('subscriber.id'), nullable=False)

  def __init__(self, message):
    self.message = message