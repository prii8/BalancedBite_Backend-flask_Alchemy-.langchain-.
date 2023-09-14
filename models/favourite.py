from db import db
from sqlalchemy import Text

class FavModel(db.Model):
    __tablename__="favourites"

    fav_id=db.Column(db.Integer,primary_key=True)
    dish=db.Column(db.String(80))
    calories = db.Column(db.Float, nullable=False)
    carbs = db.Column(db.Float, nullable=False)
    protein = db.Column(db.Float, nullable=False)
    fat = db.Column(db.Float, nullable=False)
    image_url = db.Column(Text, nullable=False)
    user_id=db.Column(db.Integer,db.ForeignKey("users.user_id"),unique=False,nullable=False)
    user=db.Relationship("UserModel",back_populates="fav")

    

