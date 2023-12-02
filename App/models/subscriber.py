from App.database import db
from .publisher import *

class Subscriber(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    publisher_id = db.Column(db.Integer, db.ForeignKey('publisher.id'), nullable=False)
    state = db.relationship('State', backref="subscriber", lazy=True)

    def __init__(self, name, publisher_id):
      self.publisher_id =  publisher_id
      self.name = name
  
    def update(self):
      print(f'{self.name}: updating')
      #self.state.append(State)
      db.session.add(self)
      db.session.commit()