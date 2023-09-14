from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError

from db import db
from models.recipe import RecipeModel
from schemas import RecipeSchema


blp = Blueprint("Recipe", "recipe", description="Operations on recipe table")





@blp.route("/recipe")
class RecipeList(MethodView):
    @blp.response(200, RecipeSchema(many=True))
    def get(self):
        raise NotImplementedError("Listing items is not implemented.")

    @blp.arguments(RecipeSchema)
    @blp.response(201, RecipeSchema)
    def post(self, meal_data):
        meal = RecipeModel(**meal_data)

        try:
            db.session.add(meal)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="An error occurred while inserting the item.")

        return meal