from json import loads
import json
import logging
from flask.views import MethodView
from flask_smorest import Blueprint, abort
import requests
from sqlalchemy.exc import SQLAlchemyError
from langchainPrompts.dietplangenerator import Breakfastplan, Dinnerplan, Elevensesplan, Eveningsnackplan, Lunchplan, MacroBreakfastplan, MacroDinnerplan, MacroElevensesplan, MacroEveningsnackplan, MacroLunchplan, Macromealplan, MealswapBudget, Recipe, mealplan
from flask import jsonify, request
from langchainPrompts.macrovlaues import macrovalues
from models.diet import DietModel
from models.recipe import RecipeModel
from models.user import UserModel
from models.user_log import User_log_model
from db import db
from models import UserModel
from flask_cors import cross_origin





from models.user_log import User_log_model


blp = Blueprint("Langchain", "langchain", description="Operations using langchain")

@blp.route("/user/langchain/<int:user_id>", methods=["PUT"])
def add_additional_user_data(user_id):
    user = UserModel.query.get(user_id)
    if not user:
        return jsonify({"message": "User not found"}), 404

    data = request.get_json()
    for key, value in data.items():
        if hasattr(user, key):
            setattr(user, key, value)
    db.session.commit()
    user = UserModel.query.get(user_id)
    user_data = {
        "id":user.id,
        "age": user.age,
        "gender": user.gender,
        "height": user.height,
        "weight": user.weight,
        "activity_level": user.activity_level,
        "end_goal": user.end_goal,
    }
    macro_data = macrovalues(
        user_data["age"],
        user_data["weight"],
        user_data["height"],
        user_data["gender"],
        user_data["activity_level"],
        user_data["end_goal"]
    )

    macro_data_dict = loads(macro_data)
    caloriee = macro_data_dict.get('Calorie')
    carbss = macro_data_dict.get('Carbs')
    proteins = macro_data_dict.get('Protein')
    fatss = macro_data_dict.get('Fats')
    print(macro_data_dict.get('carbs'))
    if not all([caloriee, carbss, proteins, fatss]):
        return jsonify({"message": "Some values are missing in macrovalues output"}), 400
    

   
    macro = {
       
        "calorie": caloriee ,
        "carbs": carbss,
        "protein":proteins,
        "fats": fatss,
    }

    for key, value in macro.items():
        if hasattr(user, key):
            setattr(user, key, value)
    db.session.commit()



    return jsonify({
       "user":user.serialize(),
        }), 200




@blp.route("/get_meal_plan/<int:user_id>", methods=["GET"])
def get_meal_plan(user_id):
    user = UserModel.query.get(user_id)
    if not user:
        return jsonify({"message": "User not found"}), 404
    new_log = User_log_model(user_id=user_id)
    db.session.add(new_log)
    db.session.commit()
    gender = user.gender
    weight = user.weight
    height = user.height
    age = user.age
    activity_level = user.activity_level
    end_goal = user.end_goal
    allergies = user.allergies
    user_type = user.diet_type
    cuisine_type = user.cuisine_type
    no_meals = user.no_meals


    meal_plan_response = mealplan(
        gender, weight, height, age, activity_level, end_goal, allergies, user_type, cuisine_type, no_meals
    )

    if isinstance(meal_plan_response, str):
        meal_plan_response = json.loads(meal_plan_response)

    diet = DietModel.query.filter_by(user_id=user_id).first()


    if not diet:
        return jsonify({"message": "Diet plan not found for the user"}), 404

  
    if not diet.meals.first():
        try:
            for meal_name, options in meal_plan_response.items():
                   for option_name, details in options.items():
                        dish = details["dish"]
                        cost = details["cost"]

                     
                        calories, carbs, protein, fat, image_url, uri =fetch_recipe_information(dish)

                       
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
                            diet_id=diet.diet_id,
                        )

                      
                        db.session.add(new_recipe)

            db.session.commit()
        except Exception as e:
            h=str(e)
            print(f"Error creating new recipe: {e}")
            return jsonify({"message": "Error creating new recipe","error":h}), 500



    return jsonify({"message": "Meal plan retrieved and stored successfully", "recipe": diet.serialize(),"userlog":new_log.serialize()}), 200



def fetch_recipe_information(meal_recipe):
    """This will fetch the recipe information like nutrients value of the dish , image url and   """

    api_url = f"https://api.edamam.com/api/recipes/v2?type=public&q={meal_recipe}&app_id=611715da&app_key=d1b48831f35de696135d9f02911b2802&imageSize=LARGE"

    try:
        response = requests.get(api_url)
        response.raise_for_status() 
        data = response.json()

        if "hits" in data and len(data["hits"]) > 0:
            recipe = data["hits"][0]["recipe"] 
            calories = recipe["calories"]
            carbs = recipe["totalNutrients"]["CHOCDF"]["quantity"]
            protein = recipe["totalNutrients"]["PROCNT"]["quantity"]
            fat = recipe["totalNutrients"]["FAT"]["quantity"]
            image_url = recipe["images"]["LARGE"]["url"]
            uri = recipe["uri"]
        else:
            calories = 300
            carbs = 40
            protein = 20
            fat = 5
            image_url = ""
            uri=""
    except requests.exceptions.RequestException as e:
        print(f"API request failed: {e}")       
        return 300, 40, 20, 5, ""

    return calories, carbs, protein, fat, image_url ,uri





@blp.route("/breakfast")
class Breakfastplangenerate(MethodView):
    def get(self):
       return Breakfastplan("female",56,1750,225,175,"reduce weight","peanuts","non-vegetarian","north indian",5)
    

@blp.route("/dinner")
class Dinnerplangenerate(MethodView):
    def get(self):
       return Dinnerplan("female",56,1750,225,175,"reduce weight","peanuts","non-vegetarian","north indian",5)
    



    


@blp.route("/snack1")
class Snackplangenerate(MethodView):
    def get(self):
       return Elevensesplan("female",56,1750,225,175,"reduce weight","peanuts","non-vegetarian","north indian",5)
    

@blp.route("/snack2")
class Eveningplangenerate(MethodView):
    def get(self):
       return Eveningsnackplan("female",56,1750,225,175,"reduce weight","peanuts","non-vegetarian","north indian",5)
    



#new prompts 
@blp.route("/macrobreakfast")
class MacroBreakfastplangenerate(MethodView):
    def get(self):
       fats=56//4
       calorie=1750//4
       protein=225//4
       carbs=175//4
       return MacroBreakfastplan("female",fats,calorie,protein,carbs,"reduce weight","peanuts","non-vegetarian","north indian")
    


@blp.route("/macromorningsnack")
class MacroMorningsnackplangenerate(MethodView):
    def get(self):
       
       fats=56//4
       calorie=1750//4
       protein=225//4
       carbs=175//4
       return MacroElevensesplan("female",fats,calorie,protein,carbs,"reduce weight","peanuts","non-vegetarian","north indian")




@blp.route("/macrolunch")
class MacroLunchplangenerate(MethodView):
    def get(self):
       fats=56//4
       calorie=1750//4
       protein=225//4
       carbs=175//4
       return MacroLunchplan("female",fats,calorie,protein,carbs,"reduce weight","peanuts","non-vegetarian","north indian")
    
@blp.route("/macrodinner")
class MacroEveningsnackplangenerate(MethodView):
    def get(self):
       fats=56//5
       calorie=1750//5
       protein=225//5
       carbs=175//5
       return MacroDinnerplan("female",fats,calorie,protein,carbs,"reduce weight","peanuts","non-vegetarian","north indian")


@blp.route("/macroeveningsnack")
class MacroDinnerplangenerate(MethodView):
    def get(self):
       fats=56//4
       calorie=1750//4
       protein=225//4
       carbs=175//4
       return MacroEveningsnackplan("female",fats,calorie,protein,carbs,"reduce weight","peanuts","non-vegetarian","north indian")
    



@blp.route("/recipe")
class Recipegenerater(MethodView):
    def get(self):
       return Recipe("Grilled Chicken Skewers")