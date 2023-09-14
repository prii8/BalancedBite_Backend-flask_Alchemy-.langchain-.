from datetime import datetime, timedelta
from sqlalchemy.exc import SQLAlchemyError
from flask import jsonify, request
from flask_smorest import Blueprint, abort
from models.user_log import User_log_model
from db import db

userl = Blueprint("user_log", __name__, description="Operations for logging users progress")


def modify_user_logs(user_log,input_data):
        
        if 'calories_log' in input_data:
            user_log.calories_log += input_data['calories_log']

        if 'carbs_log' in input_data:
            user_log.carbs_log += input_data['carbs_log']

        if 'proteins_log' in input_data:
            user_log.proteins_log += input_data['proteins_log']

        if 'fats_log' in input_data:
            user_log.fats_log += input_data['fats_log']

        
        if 'water_intake' in input_data:
            user_log.water_intake += input_data['water_intake']

        if 'breakfast_expense' in input_data:
            user_log.breakfast_expense += input_data['breakfast_expense']

        if 'lunch_expense' in input_data:
            user_log.lunch_expense += input_data['lunch_expense']
        
        if 'dinner_expense' in input_data:
            user_log.dinner_expense += input_data['dinner_expense']
        
        if 'morningsnack_expense' in input_data:
            user_log.morningsnack_expense += input_data['morningsnack_expense']
        
        if 'eveningsnack_expense' in input_data:
            user_log.eveningsnack_expense += input_data['eveningsnack_expense']

        

        db.session.commit()

        return user_log.serialize()


@userl.route('/update_user_log/<int:user_log_id>', methods=['PUT'])
def update_user_log(user_log_id):
    """Function is used to update the user_log ,the response will we get will be added in the previous response  """
    try:
        request_data = request.get_json()
        user_log = User_log_model.query.get(user_log_id)
        
        if user_log:
            updated_log = modify_user_logs(user_log, request_data)
            return jsonify(updated_log), 200
        else:
            return jsonify({'message': 'User log with the specified ID does not exist.'}), 404
    except SQLAlchemyError as e:
        error_message = f"An error occurred: {str(e)}"
        abort(500, message=error_message)


@userl.route('/get_all_user_logs', methods=['GET'])
def get_all_user_logs():
    """ Function to get all the user_logs """
    try:
        user_logs = User_log_model.query.all()
        serialized_logs = [log.serialize() for log in user_logs]
        return jsonify(serialized_logs), 200
    except Exception as e:
        error_message = f"An error occurred: {str(e)}"
        return jsonify({"message": error_message}), 500



@userl.route('/get_user_logs/<int:user_log_id>', methods=['GET'])
def get_user_log(user_log_id):
    """Function is used to user_log on the basis of the user_log_id"""
    try:
        user_log = User_log_model.query.get(user_log_id)
        if user_log:
            return jsonify(user_log.serialize()), 200
        else:
            return jsonify({'message': 'User log with the specified ID does not exist.'}), 404
    except SQLAlchemyError as e:
        error_message = f"An error occurred: {str(e)}"
        abort(500, message=error_message)



@userl.route('/user_logs', methods=['POST'])
def create_user_log():
    """ Fuction is used to create a user_log (just for the purpose of testing)"""
    try:
        data = request.get_json()  

        # Ensure 'user_id' is present in the data
        # if 'user_id' not in data:
        #     return jsonify({'error': 'Missing user_id'}), 400  # 400 indicates "Bad Request"

       
        new_user_log = User_log_model(**data)
        

        
        db.session.add(new_user_log)
        db.session.commit()

        return jsonify(new_user_log.serialize()), 201  
    except Exception as e:
        return jsonify({'error': str(e)}), 500  





#Endpoints to get the latest user_logs related to carbs ,protein ,calorie and fats


@userl.route('/carbs/<int:user_id>', methods=['GET'])
def get_latest_carbs_logs(user_id):
    """ Functon is used to get the the latest 7 carbs_log of the user """
    try:
        # Retrieve the latest 7 user logs based on timestamp
        latest_logs = User_log_model.query.filter_by(user_id=user_id).order_by(User_log_model.timestamp.desc()).limit(7).all()

        # Create a list of dictionaries containing timestamps and carbs values
        timestamps_and_carbs = [{'timestamp': log.timestamp, 'calories': log.carbs_log} for log in latest_logs]

        return jsonify(timestamps_and_carbs), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500




@userl.route('/calories/<int:user_id>', methods=['GET'])
def get_latest_calories_logs(user_id):
    """ Functon is used to get the the latest 7 calories_log of the user """
    try:
        # Retrieve the latest 7 user logs based on timestamp
        latest_logs = User_log_model.query.filter_by(user_id=user_id).order_by(User_log_model.timestamp.desc()).limit(7).all()

        # Create a list of dictionaries containing timestamps and calories values
        timestamps_and_calories = [{'timestamp': log.timestamp, 'calories': log.calories_log} for log in latest_logs]

        return jsonify(timestamps_and_calories), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500




@userl.route('/proteins/<int:user_id>', methods=['GET'])
def get_latest_proteins_logs(user_id):
    """ Functon is used to get the the latest 7 proteins_log of the user """
    try:
        # Retrieve the latest 7 user logs based on timestamp
        latest_logs = User_log_model.query.filter_by(user_id=user_id).order_by(User_log_model.timestamp.desc()).limit(7).all()

        # Create a list of dictionaries containing timestamps and calories values
        timestamps_and_proteins = [{'timestamp': log.timestamp, 'calories': log.proteins_log} for log in latest_logs]

        return jsonify(timestamps_and_proteins), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    



@userl.route('/fats/<int:user_id>', methods=['GET'])
def get_latest_fats_logs(user_id):
    """ Functon is used to get the the latest 7 fats_log of the user """
    try:
        # Retrieve the latest 7 user logs based on timestamp
        latest_logs = User_log_model.query.filter_by(user_id=user_id).order_by(User_log_model.timestamp.desc()).limit(7).all()

        # Create a list of dictionaries containing timestamps and calories values
        timestamps_and_fats = [{'timestamp': log.timestamp, 'calories': log.fats_log} for log in latest_logs]

        return jsonify(timestamps_and_fats), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    






# ENDPOINTS for AVERAGE of carbs,calorie,protein ,fats and water intake  of the user 


@userl.route('/avg/carbs/<int:user_id>', methods=['GET'])
def get_average_carbs(user_id):
    try:
        # Retrieve all user logs for the given user ID
        user_logs = User_log_model.query.filter_by(user_id=user_id).all()

        # Calculate the total carbs and count of user logs
        total_carbs = sum(log.carbs_log for log in user_logs)
        log_count = len(user_logs)

        # Calculate the average carbs
        if log_count > 0:
            average_carbs = total_carbs / log_count
        else:
            average_carbs = 0

        return jsonify({'average_carbs': average_carbs}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    


@userl.route('/avg/calories/<int:user_id>', methods=['GET'])
def get_average_calories(user_id):
    try:
        # Retrieve all user logs for the given user ID
        user_logs = User_log_model.query.filter_by(user_id=user_id).all()

        # Calculate the total calorie and count of user logs
        total_calories = sum(log.calories_log for log in user_logs)
        log_count = len(user_logs)

        # Calculate the average calorie
        if log_count > 0:
            average_calories = total_calories / log_count
        else:
            average_calories = 0

        return jsonify({'average_calories': average_calories}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    


@userl.route('/avg/proteins/<int:user_id>', methods=['GET'])
def get_average_proteins(user_id):
    try:
        # Retrieve all user logs for the given user ID
        user_logs = User_log_model.query.filter_by(user_id=user_id).all()

        # Calculate the total protein and count of user logs
        total_proteins = sum(log.proteins_log for log in user_logs)
        log_count = len(user_logs)

        # Calculate the average proteins
        if log_count > 0:
            average_proteins = total_proteins / log_count
        else:
            average_proteins = 0

        return jsonify({'average_proteins': average_proteins}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    


@userl.route('/avg/fats/<int:user_id>', methods=['GET'])
def get_average_fats(user_id):
    try:
        # Retrieve all user logs for the given user ID
        user_logs = User_log_model.query.filter_by(user_id=user_id).all()

        # Calculate the total fats and count of user logs
        total_fats = sum(log.fats_log for log in user_logs)
        log_count = len(user_logs)

        # Calculate the average fats
        if log_count > 0:
            average_fats = total_fats / log_count
        else:
            average_fats = 0

        return jsonify({'average_carbs': average_fats}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    


@userl.route('/avg/water_intake/<int:user_id>', methods=['GET'])
def get_average_carbs(user_id):
    
    try:
        # Retrieve all user logs for the given user ID
        user_logs = User_log_model.query.filter_by(user_id=user_id).all()

        # Calculate the total water_intake and count of user logs
        total_water_intake = sum(log.water_intake for log in user_logs)
        log_count = len(user_logs)

        # Calculate the average water_intake
        if log_count > 0:
            average_water_intake = total_water_intake / log_count
        else:
            average_water_intake = 0

        return jsonify({'average_carbs': average_water_intake}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    

@userl.route('/avg/nutrition/<int:user_id>', methods=['GET'])
def get_average_nutrition(user_id):
    """ Function is used to get average consumption of carbs , calories, protein fats and water intake of the user"""
    try:
        # Retrieve all user logs for the given user ID
        user_logs = User_log_model.query.filter_by(user_id=user_id).all()

        # Calculate the sum of nutritional attributes and count of user logs
        total_carbs = sum(log.carbs_log for log in user_logs)
        total_calories = sum(log.calories_log for log in user_logs)
        total_fats = sum(log.fats_log for log in user_logs)
        total_proteins = sum(log.proteins_log for log in user_logs)
        total_water_intake = sum(log.water_intake for log in user_logs)

        log_count = len(user_logs)

        # Calculate the average nutritional values
        if log_count > 0:
            average_carbs = total_carbs / log_count
            average_calories = total_calories / log_count
            average_fats = total_fats / log_count
            average_proteins = total_proteins / log_count
            average_water_intake = total_water_intake / log_count
        else:
            average_carbs = average_calories = average_fats = average_proteins = average_water_intake = 0

        return jsonify({
            'average_carbs': average_carbs,
            'average_calories': average_calories,
            'average_fats': average_fats,
            'average_proteins': average_proteins,
            'average_water_intake': average_water_intake
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500




#ENDPOINT for total expenditure on food 


@userl.route('/avg/expenditure/<int:user_id>', methods=['GET'])
def get_average_expenditure(user_id):
    """Function is used to get the total expense of all categories (that are breakfast ,lunch , dinner ,evening snack and morning snack") of the user """
    try:
        # Retrieve all user logs for the given user ID
        user_logs = User_log_model.query.filter_by(user_id=user_id).all()

        # Create a list to hold the results
        result = []

        # Meal categories and their corresponding attributes
        meal_categories = [
            ('breakfast', 'breakfast_expense'),
            ('lunch', 'lunch_expense'),
            ('dinner', 'dinner_expense'),
            ('snack1', 'morningsnack_expense'),
            ('snack2', 'eveningsnack_expense')
        ]

        # Loop through meal categories and calculate total expenditures
        for category, attribute in meal_categories:
            total_amount = sum(getattr(log, attribute, 0) for log in user_logs)
            result.append({'name': category, 'amount': total_amount})

        
        return jsonify(result), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500