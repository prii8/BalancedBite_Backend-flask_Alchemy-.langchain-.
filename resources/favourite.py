from flask import jsonify
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError

from db import db
from models import FavModel
from schemas import  FavSchema

blp = Blueprint("Fav", "fav", description="Operations on fav")





@blp.route("/fav")
class FavList(MethodView):
    @blp.response(200, FavSchema(many=True))
    def get(self):
        """To get all the favourites in the fav table"""
        return FavModel.query.all()

    @blp.arguments(FavSchema)
    @blp.response(201, FavSchema)
    def post(self, fav_data):
        """ adding favourite you send the user_id in the response"""
        fav = FavModel(**fav_data)

        try:
            db.session.add(fav)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="An error occurred while inserting the item.")

        return fav
    

@blp.route("/fav/<int:fav_id>")
class Fav(MethodView):

    def delete(self,fav_id):
        """Function is used to delete fav using fav_id"""
        fav=FavModel.query.get_or_404(fav_id)
        db.session.delete(fav)
        db.session.commit()
        return {"message":"Recipr delete from favourite list"}
    

@blp.route("/user/fav/<int:user_id>")
class UserFav(MethodView):

    @blp.response(200,FavSchema(many=True))
    def get(self,user_id):
        """this function will be used to get fav of the user"""

        user_favs=FavModel.query.filter_by(user_id=user_id).all()
        return user_favs
        