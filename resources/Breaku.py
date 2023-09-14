import json
from flask import jsonify
from flask.views import MethodView
from flask_smorest import Blueprint, abort
import requests
from sqlalchemy.exc import SQLAlchemyError
from db import db
from langchainPrompts.dietplangenerator import Breakfastplan, Dinnerplan, Elevensesplan, Eveningsnackplan, Lunchplan, MacroBreakfastplan, MacroDinnerplan, MacroElevensesplan, MacroEveningsnackplan, MacroLunchplan, Recipe
from models import DietModel
from models.recipe import RecipeModel
from models.user import UserModel
from models.user_log import User_log_model
from schemas import DietSchema
import requests
from bs4 import BeautifulSoup




blp = Blueprint("BreakU", "breakU", description="Operations on diets")

@blp.route("/creatediet/<int:user_id>")
def breakDietCreate(user_id):
    try:
        user = UserModel.query.get(user_id)
        if not user:
            return jsonify({"message": "User not found"}), 404
       

        new_diet = DietModel(user_id=user_id)
        new_log = User_log_model(user_id=user_id)
        db.session.add(new_diet)
        db.session.add(new_log)
        db.session.commit()

        calorie = user.calorie
        carbs = user.carbs
        protein = user.protein 
        fats = user.fats
        allergies = user.allergies
        diet_type = user.user_type
        cuisine = user.cuisine_type
        meals = user.no_meals
        goal = user.end_goal 
        gender = user.gender
      

        meal_plan_response =  Breakfastplan(gender, fats, calorie, protein, carbs, goal, allergies, diet_type, cuisine, meals)
    
        if isinstance(meal_plan_response, str):
            meal_plan_response = json.loads(meal_plan_response)


        recipes_to_insert = []
        for meal_name, options in meal_plan_response.items():
            for option_name, details in options.items():
                dish = details["dish"]
                cost = details["cost"]
                carbs= details["carbs"]
                protein = details["protein"]
                fats= details["fats"]
                calorie= details["calorie"]



                image_url, uri = fetch_recipe_information(dish)

                new_recipe = RecipeModel(
                    meal_type=meal_name.lower(),
                    recipe_name=dish,
                    calories=calorie,
                    carbs=carbs,
                    protein=protein,
                    fat=fats,
                    image_url=image_url,
                    price=cost,
                    uri=uri,
                    diet_id=new_diet.diet_id,
                )

                recipes_to_insert.append(new_recipe)

        db.session.bulk_save_objects(recipes_to_insert)
        db.session.commit()

        return jsonify({"user_log": new_log.serialize(),"diet": new_diet.breakfast()}), 200
    except SQLAlchemyError as e:
        error_message = f"An error occurred: {str(e)}"
        abort(500, message=error_message)





@blp.route("/breakfast/<int:user_id>/<int:diet_id>")
def breakDietCreate(user_id,diet_id):
    try:
        user = UserModel.query.get(user_id)
        if not user:
            return jsonify({"message": "User not found"}), 404
     
        diet = DietModel.query.get(diet_id)
        if not diet:
            return jsonify({"message": "Diet not found"}), 404

        existing_breakfast = DietModel.query.filter_by(user_id=user_id, diet_id=diet_id).first()
        existing_recipes = RecipeModel.query.filter_by(diet_id=diet_id, meal_type="breakfast").all()

        
        if existing_recipes:
            meal_plan_response = existing_breakfast.breakfast()
            return jsonify({"diet": meal_plan_response}), 200
        else:
            calorie = user.calorie
            carbs = user.carbs
            protein = user.protein 
            fats = user.fats
            allergies = user.allergies
            diet_type = user.user_type
            cuisine = user.cuisine_type
            meals = user.no_meals
            goal = user.end_goal 
            gender = user.gender
        

            meal_plan_response =  Breakfastplan(gender, fats, calorie, protein, carbs, goal, allergies, diet_type, cuisine, meals)
        
            if isinstance(meal_plan_response, str):
                meal_plan_response = json.loads(meal_plan_response)


            diet = DietModel.query.filter_by(user_id=user_id, diet_id=diet_id).first()

            recipes_to_insert = []
            for meal_name, options in meal_plan_response.items():
                for option_name, details in options.items():
                    dish = details["dish"]
                    cost = details["cost"]
                    carbs= details["carbs"]
                    protein = details["protein"]
                    fats= details["fats"]
                    calorie= details["calorie"]



                    image_url, uri = fetch_recipe_information(dish)

                    new_recipe = RecipeModel(
                        meal_type=meal_name.lower(),
                        recipe_name=dish,
                        calories=calorie,
                        carbs=carbs,
                        protein=protein,
                        fat=fats,
                        image_url=image_url,
                        price=cost,
                        uri=uri,
                        diet_id=diet_id,
                    )

                    recipes_to_insert.append(new_recipe)

            db.session.bulk_save_objects(recipes_to_insert)
            db.session.commit()

            return jsonify({"diet": diet.breakfast()}), 200
        
    except SQLAlchemyError as e:
        error_message = f"An error occurred: {str(e)}"
        abort(500, message=error_message)





    
@blp.route("/lunch/<int:user_id>/<int:diet_id>")
def LunchDietCreate(user_id,diet_id):
    try:
        user = UserModel.query.get(user_id)
        if not user:
            return jsonify({"message": "User not found"}), 404

        diet = DietModel.query.get(diet_id)
        if not diet:
            return jsonify({"message": "Diet not found"}), 404

        existing_lunch = DietModel.query.filter_by(user_id=user_id, diet_id=diet_id).first()
        existing_recipes = RecipeModel.query.filter_by(diet_id=diet_id, meal_type="lunch").all()

        
        if existing_recipes:
            meal_plan_response = existing_lunch.lunch()
            return jsonify({"diet": meal_plan_response}), 200
        else:
            calorie = user.calorie
            carbs = user.carbs
            protein = user.protein 
            fats = user.fats
            allergies = user.allergies
            diet_type = user.user_type
            cuisine = user.cuisine_type
            meals = user.no_meals
            goal = user.end_goal 
            gender = user.gender

            meal_plan_response =  Lunchplan(gender, fats, calorie, protein, carbs, goal, allergies, diet_type, cuisine, meals)
        
            if isinstance(meal_plan_response, str):
                meal_plan_response = json.loads(meal_plan_response)

            diet = DietModel.query.filter_by(user_id=user_id, diet_id=diet_id).first()

            recipes_to_insert = []
            for meal_name, options in meal_plan_response.items():
                for option_name, details in options.items():
                    dish = details["dish"]
                    cost = details["cost"]
                    carbs= details["carbs"]
                    protein = details["protein"]
                    fats= details["fats"]
                    calorie= details["calorie"]



                    image_url, uri = fetch_recipe_information(dish)

                    new_recipe = RecipeModel(
                        meal_type=meal_name.lower(),
                        recipe_name=dish,
                        calories=calorie,
                        carbs=carbs,
                        protein=protein,
                        fat=fats,
                        image_url=image_url,
                        price=cost,
                        uri=uri,
                        diet_id=diet_id,
                    )

                    recipes_to_insert.append(new_recipe)

            db.session.bulk_save_objects(recipes_to_insert)
            db.session.commit()

            return jsonify({"diet": diet.lunch()}), 200
    except SQLAlchemyError as e:
        error_message = f"An error occurred: {str(e)}"
        abort(500, message=error_message)





@blp.route("/dinner/<int:user_id>/<int:diet_id>")
def DinnerDietCreate(user_id,diet_id):
    try:
        user = UserModel.query.get(user_id)
        if not user:
            return jsonify({"message": "User not found"}), 404

     
        diet = DietModel.query.get(diet_id)
        if not diet:
            return jsonify({"message": "Diet not found"}), 404

        existing_dinner = DietModel.query.filter_by(user_id=user_id, diet_id=diet_id).first()
        existing_recipes = RecipeModel.query.filter_by(diet_id=diet_id, meal_type="dinner").all()

    
        if existing_recipes:
            meal_plan_response = existing_dinner.dinner()
            return jsonify({"diet": meal_plan_response}), 200
        else:
            calorie = user.calorie
            carbs = user.carbs
            protein = user.protein 
            fats = user.fats
            allergies = user.allergies
            diet_type = user.user_type
            cuisine = user.cuisine_type
            meals = user.no_meals
            goal = user.end_goal 
            gender = user.gender

            meal_plan_response =  Dinnerplan(gender, fats, calorie, protein, carbs, goal, allergies, diet_type, cuisine, meals)
        
            if isinstance(meal_plan_response, str):
                meal_plan_response = json.loads(meal_plan_response)

            diet = DietModel.query.filter_by(user_id=user_id,diet_id=diet_id).first()

            recipes_to_insert = []
            for meal_name, options in meal_plan_response.items():
                for option_name, details in options.items():
                    dish = details["dish"]
                    cost = details["cost"]
                    carbs= details["carbs"]
                    protein = details["protein"]
                    fats= details["fats"]
                    calorie= details["calorie"]



                    image_url, uri = fetch_recipe_information(dish)

                    new_recipe = RecipeModel(
                        meal_type=meal_name.lower(),
                        recipe_name=dish,
                        calories=calorie,
                        carbs=carbs,
                        protein=protein,
                        fat=fats,
                        image_url=image_url,
                        price=cost,
                        uri=uri,
                        diet_id=diet_id,
                    )

                    recipes_to_insert.append(new_recipe)

            db.session.bulk_save_objects(recipes_to_insert)
            db.session.commit()

            return jsonify({"diet": diet.dinner()}), 200
    except SQLAlchemyError as e:
        error_message = f"An error occurred: {str(e)}"
        abort(500, message=error_message)




@blp.route("/snack1/<int:user_id>/<int:diet_id>")
def SnackCreate(user_id,diet_id):
    try:
        user = UserModel.query.get(user_id)
        if not user:
            return jsonify({"message": "User not found"}), 404

        diet = DietModel.query.get(diet_id)
        if not diet:
            return jsonify({"message": "Diet not found"}), 404

        existing_snack1 = DietModel.query.filter_by(user_id=user_id, diet_id=diet_id).first()
        existing_recipes = RecipeModel.query.filter_by(diet_id=diet_id, meal_type="morningsnack").all()

    
        if existing_recipes:
            meal_plan_response = existing_snack1.snack1()
            return jsonify({"diet": meal_plan_response}), 200
        else:
            calorie = user.calorie
            carbs = user.carbs
            protein = user.protein 
            fats = user.fats
            allergies = user.allergies
            diet_type = user.user_type
            cuisine = user.cuisine_type
            meals = user.no_meals
            goal = user.end_goal 
            gender = user.gender

            meal_plan_response = Elevensesplan(gender, fats, calorie, protein, carbs, goal, allergies, diet_type, cuisine, meals)
        
            if isinstance(meal_plan_response, str):
                meal_plan_response = json.loads(meal_plan_response)

           
            
            diet = DietModel.query.filter_by(user_id=user_id,diet_id=diet_id).first()
            recipes_to_insert = []
            for meal_name, options in meal_plan_response.items():
                for option_name, details in options.items():
                    dish = details["dish"]
                    cost = details["cost"]
                    carbs= details["carbs"]
                    protein = details["protein"]
                    fats= details["fats"]
                    calorie= details["calorie"]



                    image_url, uri = fetch_recipe_information(dish)

                    new_recipe = RecipeModel(
                        meal_type=meal_name.lower(),
                        recipe_name=dish,
                        calories=calorie,
                        carbs=carbs,
                        protein=protein,
                        fat=fats,
                        image_url=image_url,
                        price=cost,
                        uri=uri,
                        diet_id=diet_id,
                    )

                    recipes_to_insert.append(new_recipe)

            db.session.bulk_save_objects(recipes_to_insert)
            db.session.commit()

            return jsonify({"diet": diet.snack1(),}), 200
    except SQLAlchemyError as e:
        error_message = f"An error occurred: {str(e)}"
        abort(500, message=error_message)




@blp.route("/snack2/<int:user_id>/<int:diet_id>")
def EveningDietCreate(user_id,diet_id):
    try:
        user = UserModel.query.get(user_id)
        if not user:
            return jsonify({"message": "User not found"}), 404

        diet = DietModel.query.get(diet_id)
        if not diet:
            return jsonify({"message": "Diet not found"}), 404

        existing_snack2 = DietModel.query.filter_by(user_id=user_id, diet_id=diet_id).first()
        existing_recipes = RecipeModel.query.filter_by(diet_id=diet_id, meal_type="eveningsnack").all()

        
        if existing_recipes:
            meal_plan_response = existing_snack2.snack2()
            return jsonify({"diet": meal_plan_response}), 200
        else:
            calorie = user.calorie
            carbs = user.carbs
            protein = user.protein 
            fats = user.fats
            allergies = user.allergies
            diet_type = user.user_type
            cuisine = user.cuisine_type
            meals = user.no_meals
            goal = user.end_goal 
            gender = user.gender

            meal_plan_response =  Eveningsnackplan(gender, fats, calorie, protein, carbs, goal, allergies, diet_type, cuisine, meals)
        
            if isinstance(meal_plan_response, str):
                meal_plan_response = json.loads(meal_plan_response)

            diet = DietModel.query.filter_by(user_id=user_id,diet_id=diet_id).first()
            
            recipes_to_insert = []
            for meal_name, options in meal_plan_response.items():
                for option_name, details in options.items():
                    dish = details["dish"]
                    cost = details["cost"]
                    carbs= details["carbs"]
                    protein = details["protein"]
                    fats= details["fats"]
                    calorie= details["calorie"]

                    image_url, uri = fetch_recipe_information(dish)

                    new_recipe = RecipeModel(
                        meal_type=meal_name.lower(),
                        recipe_name=dish,
                        calories=calorie,
                        carbs=carbs,
                        protein=protein,
                        fat=fats,
                        image_url=image_url,
                        price=cost,
                        uri=uri,
                        diet_id=diet_id,
                    )

                    recipes_to_insert.append(new_recipe)

            db.session.bulk_save_objects(recipes_to_insert)
            db.session.commit()

            return jsonify({"diet": diet.snack2(),}), 200  
    except SQLAlchemyError as e:
        error_message = f"An error occurred: {str(e)}"
        abort(500, message=error_message)


def fetch_recipe_information(meal_recipe):
    api_url = f"https://api.edamam.com/api/recipes/v2?type=public&q={meal_recipe}&app_id=611715da&app_key=d1b48831f35de696135d9f02911b2802&imageSize=LARGE"

    try:
        response = requests.get(api_url)
        response.raise_for_status() 
        data = response.json()

        if "hits" in data and len(data["hits"]) > 0:
            recipe = data["hits"][0]["recipe"] 
            image_url = recipe["images"]["LARGE"]["url"]
            uri = recipe["uri"]
        else:
            image_url = fetch_bing_image_link(meal_recipe)
            uri="http://www.edamam.com/ontologies/edamam.owl#recipe_4e47d7b853b99348e7c743d2523ca714"
    except requests.exceptions.RequestException as e:
        print(f"API request failed: {e}")       
        return 300, 40, 20, 5, ""

    return image_url ,uri

def fetch_bing_image_link(query):
    url = f"https://www.bing.com/images/search?q={query.replace(' ', '%20')}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    try:
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        image_element = soup.find('img', class_='mimg')

        if image_element:
            return image_element['src'].split('?')[0]
        else:
            return None
    except Exception as e:
        print("Error:", e)
        return None





@blp.route("/Macrocreatediet/<int:user_id>")
def breakDietCreat(user_id):
    
    try:
        user = UserModel.query.get(user_id)
        if not user:
            return jsonify({"message": "User not found"}), 404
        
     

        new_diet = DietModel(user_id=user_id)
        new_log = User_log_model(user_id=user_id)
        db.session.add(new_diet)
        db.session.add(new_log)
        db.session.commit()

       
        allergies = user.allergies
        diet_type = user.user_type
        cuisine = user.cuisine_type
        meals = user.no_meals
        goal = user.end_goal 
        gender = user.gender
        calorie = user.calorie//meals
        carbs = user.carbs//meals
        protein = user.protein//meals
        fats = user.fats//meals
      

        meal_plan_response =  MacroBreakfastplan(gender, fats, calorie, protein, carbs, goal, allergies, diet_type, cuisine)
    
        if isinstance(meal_plan_response, str):
            meal_plan_response = json.loads(meal_plan_response)


        recipes_to_insert = []
        for meal_name, options in meal_plan_response.items():
            for option_name, details in options.items():
                dish = details["dish"]
                cost = details["cost"]
                carbs= details["carbs"]
                protein = details["protein"]
                fats= details["fats"]
                calorie= details["calorie"]



                image_url, uri = fetch_recipe_information(dish)

                new_recipe = RecipeModel(
                    meal_type=meal_name.lower(),
                    recipe_name=dish,
                    calories=calorie,
                    carbs=carbs,
                    protein=protein,
                    fat=fats,
                    image_url=image_url,
                    price=cost,
                    uri=uri,
                    diet_id=new_diet.diet_id,
                )

                recipes_to_insert.append(new_recipe)

        db.session.bulk_save_objects(recipes_to_insert)
        db.session.commit()

        return jsonify({"user_log": new_log.serialize(),"diet": new_diet.breakfast()}), 200
    except SQLAlchemyError as e:
        error_message = f"An error occurred: {str(e)}"
        abort(500, message=error_message)

@blp.route("/Macrobreakfast/<int:user_id>/<int:diet_id>")
def breakDietCrea(user_id,diet_id):
    try:
        user = UserModel.query.get(user_id)
        if not user:
            return jsonify({"message": "User not found"}), 404
     
        diet = DietModel.query.get(diet_id)
        if not diet:
            return jsonify({"message": "Diet not found"}), 404

        existing_breakfast = DietModel.query.filter_by(user_id=user_id, diet_id=diet_id).first()
        existing_recipes = RecipeModel.query.filter_by(diet_id=diet_id, meal_type="breakfast").all()

        
        if existing_recipes:
            meal_plan_response = existing_breakfast.breakfast()
            return jsonify({"diet": meal_plan_response}), 200
        else:
            calorie = user.calorie
            carbs = user.carbs
            protein = user.protein 
            fats = user.fats
            allergies = user.allergies
            diet_type = user.user_type
            cuisine = user.cuisine_type
            meals = user.no_meals
            goal = user.end_goal 
            gender = user.gender
        

            meal_plan_response =  Breakfastplan(gender, fats, calorie, protein, carbs, goal, allergies, diet_type, cuisine, meals)
        
            if isinstance(meal_plan_response, str):
                meal_plan_response = json.loads(meal_plan_response)

            
            diet = DietModel.query.filter_by(user_id=user_id, diet_id=diet_id).first()

            recipes_to_insert = []
            for meal_name, options in meal_plan_response.items():
                for option_name, details in options.items():
                    dish = details["dish"]
                    cost = details["cost"]
                    carbs= details["carbs"]
                    protein = details["protein"]
                    fats= details["fats"]
                    calorie= details["calorie"]



                    image_url, uri = fetch_recipe_information(dish)

                    new_recipe = RecipeModel(
                        meal_type=meal_name.lower(),
                        recipe_name=dish,
                        calories=calorie,
                        carbs=carbs,
                        protein=protein,
                        fat=fats,
                        image_url=image_url,
                        price=cost,
                        uri=uri,
                        diet_id=diet_id,
                    )

                    recipes_to_insert.append(new_recipe)

            db.session.bulk_save_objects(recipes_to_insert)
            db.session.commit()

            return jsonify({"diet": diet.breakfast()}), 200
        
    except SQLAlchemyError as e:
        error_message = f"An error occurred: {str(e)}"
        abort(500, message=error_message)





    
@blp.route("/Macrolunch/<int:user_id>/<int:diet_id>")
def LunchDietCreat(user_id,diet_id):
    try:
        user = UserModel.query.get(user_id)
        if not user:
            return jsonify({"message": "User not found"}), 404

        diet = DietModel.query.get(diet_id)
        if not diet:
            return jsonify({"message": "Diet not found"}), 404

        existing_lunch = DietModel.query.filter_by(user_id=user_id, diet_id=diet_id).first()
        existing_recipes = RecipeModel.query.filter_by(diet_id=diet_id, meal_type="lunch").all()

        
        if existing_recipes:
            meal_plan_response = existing_lunch.lunch()
            return jsonify({"diet": meal_plan_response}), 200
        else:
            
            allergies = user.allergies
            diet_type = user.user_type
            cuisine = user.cuisine_type
            meals = user.no_meals
            goal = user.end_goal 
            gender = user.gender
            calorie = user.calorie//meals
            carbs = user.carbs//meals
            protein = user.protein//meals
            fats = user.fats//meals

            meal_plan_response =  MacroLunchplan(gender, fats, calorie, protein, carbs, goal, allergies, diet_type, cuisine)
        
            if isinstance(meal_plan_response, str):
                meal_plan_response = json.loads(meal_plan_response)

            diet = DietModel.query.filter_by(user_id=user_id, diet_id=diet_id).first()

            recipes_to_insert = []
            for meal_name, options in meal_plan_response.items():
                for option_name, details in options.items():
                    dish = details["dish"]
                    cost = details["cost"]
                    carbs= details["carbs"]
                    protein = details["protein"]
                    fats= details["fats"]
                    calorie= details["calorie"]



                    image_url, uri = fetch_recipe_information(dish)

                    new_recipe = RecipeModel(
                        meal_type=meal_name.lower(),
                        recipe_name=dish,
                        calories=calorie,
                        carbs=carbs,
                        protein=protein,
                        fat=fats,
                        image_url=image_url,
                        price=cost,
                        uri=uri,
                        diet_id=diet_id,
                    )

                    recipes_to_insert.append(new_recipe)

            db.session.bulk_save_objects(recipes_to_insert)
            db.session.commit()

            return jsonify({"diet": diet.lunch()}), 200
    except SQLAlchemyError as e:
        error_message = f"An error occurred: {str(e)}"
        abort(500, message=error_message)

@blp.route("/Macrodinner/<int:user_id>/<int:diet_id>")
def DinnerDietCreat(user_id,diet_id):
    try:
        user = UserModel.query.get(user_id)
        if not user:
            return jsonify({"message": "User not found"}), 404

     
        diet = DietModel.query.get(diet_id)
        if not diet:
            return jsonify({"message": "Diet not found"}), 404

        existing_dinner = DietModel.query.filter_by(user_id=user_id, diet_id=diet_id).first()
        existing_recipes = RecipeModel.query.filter_by(diet_id=diet_id, meal_type="dinner").all()

    
        if existing_recipes:
            meal_plan_response = existing_dinner.dinner()
            return jsonify({"diet": meal_plan_response}), 200
        else:
            allergies = user.allergies
            diet_type = user.user_type
            cuisine = user.cuisine_type
            meals = user.no_meals
            goal = user.end_goal 
            gender = user.gender
            calorie = user.calorie//meals
            carbs = user.carbs//meals
            protein = user.protein//meals 
            fats = user.fats//meals

            meal_plan_response =  MacroDinnerplan(gender, fats, calorie, protein, carbs, goal, allergies, diet_type, cuisine)
        
            if isinstance(meal_plan_response, str):
                meal_plan_response = json.loads(meal_plan_response)

            diet = DietModel.query.filter_by(user_id=user_id,diet_id=diet_id).first()

            recipes_to_insert = []
            for meal_name, options in meal_plan_response.items():
                for option_name, details in options.items():
                    dish = details["dish"]
                    cost = details["cost"]
                    carbs= details["carbs"]
                    protein = details["protein"]
                    fats= details["fats"]
                    calorie= details["calorie"]



                    image_url, uri = fetch_recipe_information(dish)

                    new_recipe = RecipeModel(
                        meal_type=meal_name.lower(),
                        recipe_name=dish,
                        calories=calorie,
                        carbs=carbs,
                        protein=protein,
                        fat=fats,
                        image_url=image_url,
                        price=cost,
                        uri=uri,
                        diet_id=diet_id,
                    )

                    recipes_to_insert.append(new_recipe)

            db.session.bulk_save_objects(recipes_to_insert)
            db.session.commit()

            return jsonify({"diet": diet.dinner()}), 200
    except SQLAlchemyError as e:
        error_message = f"An error occurred: {str(e)}"
        abort(500, message=error_message)


@blp.route("/Macrosnack1/<int:user_id>/<int:diet_id>")
def SnackCreat(user_id,diet_id):
    try:
        user = UserModel.query.get(user_id)
        if not user:
            return jsonify({"message": "User not found"}), 404

        diet = DietModel.query.get(diet_id)
        if not diet:
            return jsonify({"message": "Diet not found"}), 404

        existing_snack1 = DietModel.query.filter_by(user_id=user_id, diet_id=diet_id).first()
        existing_recipes = RecipeModel.query.filter_by(diet_id=diet_id, meal_type="morningsnack").all()

    
        if existing_recipes:
            meal_plan_response = existing_snack1.snack1()
            return jsonify({"diet": meal_plan_response}), 200
        else:
            allergies = user.allergies
            diet_type = user.user_type
            cuisine = user.cuisine_type
            meals = user.no_meals
            goal = user.end_goal 
            gender = user.gender
            calorie = user.calorie//meals
            carbs = user.carbs//meals
            protein = user.protein//meals 
            fats = user.fats//meals

            meal_plan_response = MacroElevensesplan(gender, fats, calorie, protein, carbs, goal, allergies, diet_type, cuisine)
        
            if isinstance(meal_plan_response, str):
                meal_plan_response = json.loads(meal_plan_response)

            
            diet = DietModel.query.filter_by(user_id=user_id,diet_id=diet_id).first()
            recipes_to_insert = []
            for meal_name, options in meal_plan_response.items():
                for option_name, details in options.items():
                    dish = details["dish"]
                    cost = details["cost"]
                    carbs= details["carbs"]
                    protein = details["protein"]
                    fats= details["fats"]
                    calorie= details["calorie"]



                    image_url, uri = fetch_recipe_information(dish)

                    new_recipe = RecipeModel(
                        meal_type=meal_name.lower(),
                        recipe_name=dish,
                        calories=calorie,
                        carbs=carbs,
                        protein=protein,
                        fat=fats,
                        image_url=image_url,
                        price=cost,
                        uri=uri,
                        diet_id=diet_id,
                    )

                    recipes_to_insert.append(new_recipe)

            db.session.bulk_save_objects(recipes_to_insert)
            db.session.commit()

            return jsonify({"diet": diet.snack1(),}), 200
    except SQLAlchemyError as e:
        error_message = f"An error occurred: {str(e)}"
        abort(500, message=error_message)


@blp.route("/Macrosnack2/<int:user_id>/<int:diet_id>")
def EveningDietCreat(user_id,diet_id):
    try:
        user = UserModel.query.get(user_id)
        if not user:
            return jsonify({"message": "User not found"}), 404

        diet = DietModel.query.get(diet_id)
        if not diet:
            return jsonify({"message": "Diet not found"}), 404

        existing_snack2 = DietModel.query.filter_by(user_id=user_id, diet_id=diet_id).first()
        existing_recipes = RecipeModel.query.filter_by(diet_id=diet_id, meal_type="eveningsnack").all()

        
        if existing_recipes:
            meal_plan_response = existing_snack2.snack2()
            return jsonify({"diet": meal_plan_response}), 200
        else:
           
            allergies = user.allergies
            diet_type = user.user_type
            cuisine = user.cuisine_type
            meals = user.no_meals
            goal = user.end_goal 
            gender = user.gender
            calorie = user.calorie//meals
            carbs = user.carbs//meals
            protein = user.protein//meals 
            fats = user.fats//meals

            meal_plan_response =  MacroEveningsnackplan(gender, fats, calorie, protein, carbs, goal, allergies, diet_type, cuisine)
        
            if isinstance(meal_plan_response, str):
                meal_plan_response = json.loads(meal_plan_response)

            diet = DietModel.query.filter_by(user_id=user_id,diet_id=diet_id).first()
            
            recipes_to_insert = []
            for meal_name, options in meal_plan_response.items():
                for option_name, details in options.items():
                    dish = details["dish"]
                    cost = details["cost"]
                    carbs= details["carbs"]
                    protein = details["protein"]
                    fats= details["fats"]
                    calorie= details["calorie"]

                    image_url, uri = fetch_recipe_information(dish)

                    new_recipe = RecipeModel(
                        meal_type=meal_name.lower(),
                        recipe_name=dish,
                        calories=calorie,
                        carbs=carbs,
                        protein=protein,
                        fat=fats,
                        image_url=image_url,
                        price=cost,
                        uri=uri,
                        diet_id=diet_id,
                    )

                    recipes_to_insert.append(new_recipe)

            db.session.bulk_save_objects(recipes_to_insert)
            db.session.commit()

            return jsonify({"diet": diet.snack2(),}), 200  
    except SQLAlchemyError as e:
        error_message = f"An error occurred: {str(e)}"
        abort(500, message=error_message)


@blp.route("/recipe/<int:recipe_id>")
def recipeGen(recipe_id):
    try:
        existing_recipes = RecipeModel.query.filter_by(recipe_id=recipe_id).all()
        recipe_name= [recipe.recipe_name for recipe in existing_recipes]
        responseh=Recipe(recipe_name[0])
        return jsonify({"directions":"\n"+responseh})
    except SQLAlchemyError as e:
        error_message = f"An error occurred: {str(e)}"
        abort(500, message=error_message)


