from db import db
from datetime import datetime

class UserModel(db.Model):
    __tablename__="users"

    user_id=db.Column(db.Integer,primary_key=True)
    username=db.Column(db.String(80),nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    dietplan=db.Relationship("DietModel",back_populates="user",lazy="dynamic",cascade="all, delete-orphan")
    gender = db.Column(db.String(10))
    diet_type =db.Column(db.String(50))
    age = db.Column(db.Integer)
    height = db.Column(db.Integer)
    weight = db.Column(db.Integer)
    allergies = db.Column(db.String(200))
    no_meals = db.Column(db.Integer)
    cuisine_type = db.Column(db.String(50))
    activity_level = db.Column(db.String(20))
    end_goal = db.Column(db.String(100)) 
    calorie=db.Column(db.Integer)
    carbs = db.Column(db.Integer)  # New attribute for carbs
    protein = db.Column(db.Integer)  # New attribute for protein
    fats = db.Column(db.Integer)  # New attribute for fats
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    fav=db.Relationship("FavModel",back_populates="user",lazy="dynamic",cascade="all, delete-orphan")
    user_logs = db.relationship('User_log_model', back_populates='user', lazy='dynamic')
    

    def serialize(self):
        dietplans = self.dietplan.all() if self.dietplan else []
        dietplan_list = [diet.serialize() for diet in dietplans]
        allergies = self.allergies.split(",") if self.allergies else []
        cuisine_type=self.cuisine_type.split(",") if self.cuisine_type else []
        return {
            "user_id": self.user_id,
            "username":self.username,
            "email":self.email,
            "gender": self.gender,
            "diet_type":self.diet_type,
            "age": self.age,
            "height": self.height,
            "weight": self.weight,
            "allergies": self.allergies,
            "no_meals": self.no_meals,
            "cuisine_type": self.cuisine_type,
            "activity_level": self.activity_level,
            "end_goal": self.end_goal,
            "dietplan": dietplan_list,
            "timestamp": self.timestamp.isoformat(),
            "carbs":self.carbs,
            "calories":self.calorie,
            "protien":self.protein,
            "fats":self.fats
        }
