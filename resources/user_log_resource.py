import datetime
from flask import jsonify, request
from flask_smorest import Blueprint, abort
from models.user_log import User_log_model
from db import db

blp = Blueprint("User_log", "user_log", description="Operations for logging users progress")

@blp.route('/user_log/<int:user_log_id>', methods=['PUT'])
def handle_user_log(user_log_id):
    request_data = request.get_json()
    user_log = User_log_model.query.get(user_log_id)

    if request.method == 'PUT':
        if user_log:
            modify_user_logs(user_log, request_data)
            return jsonify({'message': 'User log updated successfully.'}), 200
        else:
            return jsonify({'message': 'User log with the specified ID does not exist.'}), 404

# modify
def modify_user_logs(user_log,input_data):
        
        if 'calories_log' in input_data:
            user_log.calories_log += input_data['calories_log']

        if 'carbs_log' in input_data:
            user_log.carbs_log += input_data['carbs_log']

        if 'proteins_log' in input_data:
            user_log.proteins_log += input_data['proteins_log']

        if 'fats_log' in input_data:
            user_log.fats_log += input_data['fats_log']

        if 'current_weight' in input_data:
            user_log.weight += input_data['current_weight']

        if 'water_intake' in input_data:
            user_log.water_intake += input_data['water_intake']

        db.session.commit()

        return jsonify(user_log.serialize())


# @blp.route('/user_log/calories/7/<int:user_log_id>', methods=['GET'])
# def get_calories_last_7_days(user_id):
#     end_date = datetime.utcnow()
#     start_date = end_date - datetime.timedelta(days=7)

#     user_logs = User_log_model.query.filter_by(user_id=user_id).filter(
#         User_log_model.timestamp >= start_date,
#         User_log_model.timestamp <= end_date
#     ).all()

#     calories_last_7_days = sum(log.calories_log for log in user_logs)

#     return jsonify({"calories_last_7_days": calories_last_7_days})

# @blp.route('/user_log/calories/31/<int:user_log_id>', methods=['GET'])
# def get_calories_last_31_days(user_id):
#     end_date = datetime.utcnow()
#     start_date = end_date - datetime.timedelta(days=31)

#     user_logs = User_log_model.query.filter_by(user_id=user_id).filter(
#         User_log_model.timestamp >= start_date,
#         User_log_model.timestamp <= end_date
#     ).all()

#     calories_last_31_days = sum(log.calories_log for log in user_logs)

#     return jsonify({"calories_last_31_days": calories_last_31_days})

# @blp.route('/user_log/proteins/7/<int:user_log_id>', methods=['GET'])
# def get_proteins_last_7_days(user_id):
#     end_date = datetime.utcnow()
#     start_date = end_date - datetime.timedelta(days=7)

#     user_logs = User_log_model.query.filter_by(user_id=user_id).filter(
#         User_log_model.timestamp >= start_date,
#         User_log_model.timestamp <= end_date
#     ).all()

#     proteins_last_7_days = sum(log.proteins_log for log in user_logs)

#     return jsonify({"proteins_last_7_days": proteins_last_7_days})

# @blp.route('/user_log/proteins/31/<int:user_log_id>', methods=['GET'])
# def get_proteins_last_31_days(user_id):
#     end_date = datetime.utcnow()
#     start_date = end_date - datetime.timedelta(days=31)

#     user_logs = User_log_model.query.filter_by(user_id=user_id).filter(
#         User_log_model.timestamp >= start_date,
#         User_log_model.timestamp <= end_date
#     ).all()

#     proteins_last_31_days = sum(log.proteins_log for log in user_logs)

#     return jsonify({"proteins_last_31_days": proteins_last_31_days})


# @blp.route('/user_log/carbs/7/<int:user_log_id>', methods=['GET'])
# def get_carbs_last_7_days(user_id):
#     end_date = datetime.utcnow()
#     start_date = end_date - datetime.timedelta(days=7)

#     user_logs = User_log_model.query.filter_by(user_id=user_id).filter(
#         User_log_model.timestamp >= start_date,
#         User_log_model.timestamp <= end_date
#     ).all()

#     carbs_last_7_days = sum(log.carbs_log for log in user_logs)

#     return jsonify({"carbs_last_7_days": carbs_last_7_days})

# @blp.route('/user_log/carbs/31/<int:user_log_id>', methods=['GET'])
# def get_carbs_last_31_days(user_id):
#     end_date = datetime.utcnow()
#     start_date = end_date - datetime.timedelta(days=31)

#     user_logs = User_log_model.query.filter_by(user_id=user_id).filter(
#         User_log_model.timestamp >= start_date,
#         User_log_model.timestamp <= end_date
#     ).all()

#     carbs_last_31_days = sum(log.carbs_log for log in user_logs)

#     return jsonify({"carbs_last_31_days": carbs_last_31_days})


# @blp.route('/user_log/fats/7/<int:user_log_id>', methods=['GET'])
# def get_fats_last_7_days(user_id):
#     end_date = datetime.utcnow()
#     start_date = end_date - datetime.timedelta(days=7)

#     user_logs = User_log_model.query.filter_by(user_id=user_id).filter(
#         User_log_model.timestamp >= start_date,
#         User_log_model.timestamp <= end_date
#     ).all()

#     fats_last_7_days = sum(log.fats_log for log in user_logs)

#     return jsonify({"fats_last_7_days": fats_last_7_days})

# @blp.route('/user_log/fats/31/<int:user_log_id>', methods=['GET'])
# def get_fats_last_31_days(user_id):
#     end_date = datetime.utcnow()
#     start_date = end_date - datetime.timedelta(days=31)

#     user_logs = User_log_model.query.filter_by(user_id=user_id).filter(
#         User_log_model.timestamp >= start_date,
#         User_log_model.timestamp <= end_date
#     ).all()

#     fats_last_31_days = sum(log.fats_log for log in user_logs)

#     return jsonify({"fats_last_31_days": fats_last_31_days})

