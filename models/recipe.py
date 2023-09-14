
from datetime import datetime
from sqlalchemy import Text
from db import db

class RecipeModel(db.Model):
    __tablename__="recipe"

    recipe_id=db.Column(db.Integer,primary_key=True)
    meal_type=db.Column(db.String(80))
    recipe_name = db.Column(db.String(200), nullable=False)
    calories = db.Column(db.Float, nullable=False)
    carbs = db.Column(db.Float, nullable=False)
    protein = db.Column(db.Float, nullable=False)
    fat = db.Column(db.Float, nullable=False)
    image_url = db.Column(Text, nullable=False)
    price=db.Column(db.Integer)
    uri=db.Column(db.String(200))
    diet_id=db.Column(db.Integer,db.ForeignKey("dietplan.diet_id"),unique=False,nullable=False)
    diet=db.Relationship("DietModel",back_populates="meals")
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    def serialize(self):
        return {
            "recipe_id": self.recipe_id,
            "meal_type": self.meal_type,
            "recipe_name": self.recipe_name,
            "calories": self.calories,
            "carbs": self.carbs,
            "protein": self.protein,
            "fat": self.fat,
            "image_url": self.image_url,
            "price":self.price,
            "uri":self.uri,
            "timestamp": self.timestamp.isoformat()
        }
