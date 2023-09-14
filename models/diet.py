from datetime import datetime
from db import db

class DietModel(db.Model):
    __tablename__="dietplan"


    diet_id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    user_id=db.Column(db.Integer,db.ForeignKey("users.user_id"),unique=False,nullable=False)
    user=db.Relationship("UserModel",back_populates="dietplan")
    meals=db.Relationship("RecipeModel",back_populates="diet",lazy="dynamic",cascade="all, delete-orphan")
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    def serialize(self):
        dietplans = self.meals.all() if self.meals else []
        dietplan_list = [diet.serialize() for diet in dietplans]

        return {
            "diet_id": self.diet_id,
            "user_id": self.user_id,
            "recipe":dietplan_list,
            "timestamp": self.timestamp.isoformat()
        }
    
    def breakfast(self):
        meals = self.meals.all() if self.meals else []
        for meal in meals:
            print("Meal Type:", meal.meal_type)
        breakfast_meals = [meal.serialize() for meal in meals if meal.meal_type == "breakfast"]
        print(breakfast_meals)
        return {
            "diet_id": self.diet_id,
            "user_id": self.user_id,
            "breakfast": breakfast_meals,
            "timestamp": self.timestamp.isoformat()
        }
    
    def lunch(self):
        meals = self.meals.all() if self.meals else []
        lunch_meals = [meal.serialize() for meal in meals if meal.meal_type == "lunch"]
       

        return {
            "diet_id": self.diet_id,
            "user_id": self.user_id,
            "lunch": lunch_meals,
            "timestamp": self.timestamp.isoformat()
        }
    
    def dinner(self):
        meals = self.meals.all() if self.meals else []
        dinner_meals = [meal.serialize() for meal in meals if meal.meal_type == "dinner"]
       

        return {
            "diet_id": self.diet_id,
            "user_id": self.user_id,
            "dinner": dinner_meals,
            "timestamp": self.timestamp.isoformat()
        }
    

    def snack1(self):
        meals = self.meals.all() if self.meals else []
        snack_meals = [meal.serialize() for meal in meals if meal.meal_type == "morningsnack"]
       

        return {
            "diet_id": self.diet_id,
            "user_id": self.user_id,
            "snack1": snack_meals,
            "timestamp": self.timestamp.isoformat()
        }
    
    def snack2(self):
        meals = self.meals.all() if self.meals else []
        snack_meals = [meal.serialize() for meal in meals if meal.meal_type == "eveningsnack"]
        

        return {
            "diet_id": self.diet_id,
            "user_id": self.user_id,
            "snack2": snack_meals,
            "timestamp": self.timestamp.isoformat()
        }
    
    


   

    
   
    


