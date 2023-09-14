import json
from flask import jsonify
from flask.views import MethodView
from flask_smorest import Blueprint, abort
# from platformdirs import user_data_dir
from sqlalchemy.exc import SQLAlchemyError
import asyncio
from db import db
from langchainPrompts.dietplangenerator import Macromealplan, mealplan
from models import DietModel
from models.recipe import RecipeModel
from models.user import UserModel
from models.user_log import User_log_model
from resources.langchain import fetch_recipe_information
from schemas import DietSchema

blp = Blueprint("Diet", "diet", description="Operations on diets")
    
@blp.route("/dietplan/<int:diet_id>", methods=["GET"])
def get_dietplan(diet_id):
    diet = DietModel.query.get(diet_id)
    if diet:
        return jsonify({"diet":diet.serialize()}), 200
    else:
        return jsonify({"message": "Diet plan not found"}), 404
    


@blp.route("/dietnext1/<int:user_id>", methods=["GET"])
def get_dietplan(user_id):
    try:
        user = UserModel.query.get(user_id)
        if not user:
            return jsonify({"message": "User not found"}), 404

        new_diet = DietModel(user_id=user_id)
        db.session.add(new_diet)
        db.session.commit()
        new_log = User_log_model(user_id=user_id)
        db.session.add(new_log)
        db.session.commit()

        gender, weight, height, age, activity_level, end_goal, allergies, user_type, cuisine_type, no_meals = (
        user.gender, user.weight, user.height, user.age, user.activity_level, user.end_goal,
        user.allergies, user.diet_type, user.cuisine_type, user.no_meals
        )

        meal_plan_response = mealplan(
        gender, weight, height, age, activity_level, end_goal, allergies, user_type, cuisine_type, no_meals
       )

        if isinstance(meal_plan_response, str):
            meal_plan_response = json.loads(meal_plan_response)

        recipes_to_insert = []
        for meal_name, options in meal_plan_response.items():
            for option_name, details in options.items():
                dish = details["dish"]
                cost = details["cost"]

                calories, carbs, protein, fat, image_url, uri = fetch_recipe_information(dish)

                new_recipe = RecipeModel(
                    meal_type=meal_name,
                    recipe_name=dish,
                    calories=calories,
                    carbs=carbs,
                    protein=protein,
                    fat=fat,
                    image_url=image_url,
                    price=cost,
                    uri=uri,
                    diet_id=new_diet.diet_id,
                )

                recipes_to_insert.append(new_recipe)

        db.session.bulk_save_objects(recipes_to_insert)
        db.session.commit()

        return jsonify({"message": "Meal plan retrieved and stored successfully", "recipe": new_diet.serialize(), "user_log": new_log.serialize()}), 200

    except Exception as e:
        h = str(e)
        db.session.rollback()
        return jsonify({"message": "Internal server error", "error": h}), 500

