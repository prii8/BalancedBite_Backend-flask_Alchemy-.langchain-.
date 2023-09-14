from datetime import datetime
from sqlalchemy import Text
from db import db

from datetime import datetime
from flask_sqlalchemy import SQLAlchemy



class User_log_model(db.Model):
    __tablename__ = "user_log"
    user_log_id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    calories_log = db.Column(db.Float, default=0)
    carbs_log = db.Column(db.Float, default=0)
    proteins_log = db.Column(db.Float, default=0)
    fats_log = db.Column(db.Float, default=0)
    
    water_intake = db.Column(db.Float, default=0)
    breakfast_expense=db.Column(db.Integer,default=0)
    lunch_expense=db.Column(db.Integer,default=0)
    dinner_expense=db.Column(db.Integer,default=0)
    morningsnack_expense=db.Column(db.Integer,default=0)
    eveningsnack_expense=db.Column(db.Integer,default=0)   
    
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    price= db.Column(db.Integer, default=0)
    user = db.relationship('UserModel', back_populates='user_logs')

    def serialize(self):
        return {
            "user_log_id": self.user_log_id,
            "user_id": self.user_id,
            "timestamp": self.timestamp.isoformat(),
            "calories_log": self.calories_log,
            "carbs_log": self.carbs_log,
            "proteins_log": self.proteins_log,
            "fats_log": self.fats_log,
            
            "water_intake": self.water_intake,
            "user_id": self.user_id,
            "eveningsnack_expense":self.eveningsnack_expense,
            "morningsnack_expense":self.morningsnack_expense,
            "dinner_expense":self.dinner_expense,
            "lunch_expense":self.lunch_expense,
            "breakfast_expense":self.breakfast_expense
            
        }


