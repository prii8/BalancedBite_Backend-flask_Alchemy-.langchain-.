from flask import jsonify, request
from flask.views import MethodView
from flask_smorest import Blueprint,abort
from sqlalchemy.exc import SQLAlchemyError,IntegrityError
from db import db

from models import UserModel
from schemas import UserSchema

blp = Blueprint("Users", "susers", description="Operations on user")

@blp.route("/users")
class UserList(MethodView):
    @blp.response(200, UserSchema(many=True))
    def get(self):
        raise NotImplementedError("Listing users is not implemented.")

    @blp.arguments(UserSchema)
    @blp.response(201, UserSchema)
    def post(self, user_data):
        user = UserModel(**user_data)
        try:
            db.session.add(user)
            db.session.commit()
        except IntegrityError:
            abort(
                400,
                message="A store with that name already exists.",
            )
        except SQLAlchemyError:
            abort(500, message="An error occurred creating the store.")

        return user




@blp.route("/user", methods=["GET"])
def get_all_users():
  try:
        users = UserModel.query.all()
        return jsonify([user.serialize() for user in users]), 200
  except Exception as e:
        h=str(e)
        return jsonify({"message": "An error occurred while processing the request.","error":h}), 500


@blp.route("/user/<int:user_id>", methods=["GET"])
def get_user(user_id):
    user = UserModel.query.get(user_id)
    if user:
        return jsonify(user.serialize()), 200
    return jsonify({"message": "User not found"}), 404


@blp.route("/user", methods=["POST"])
def create_user():
    data = request.get_json()
    new_user = UserModel(**data)
    db.session.add(new_user)
    db.session.commit()
    return jsonify(new_user.serialize()), 201

@blp.route("/user/<int:user_id>", methods=["PUT"])
def update_user(user_id):
    user = UserModel.query.get(user_id)
    if not user:
        return jsonify({"message": "User not found"}), 404

    data = request.get_json()
    for key, value in data.items():
         if hasattr(user, key):
            setattr(user, key, value)

    db.session.commit()
    return jsonify(user.serialize()), 200

@blp.route("/user/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    user = UserModel.query.get(user_id)
    if user:
        db.session.delete(user)
        db.session.commit()
        return jsonify({"message": "User deleted successfully"}), 200
    return jsonify({"message": "User not found"}), 404




@blp.route("/user/<int:user_id>/preferences", methods=["GET"])
def get_user_attributes(user_id):
    user = UserModel.query.get(user_id)
    if not user:
        return jsonify({"message": "User not found"}), 404

    user_attributes = {
        "gender": user.gender,
        "age": user.age,
        "height": user.height,
        "weight": user.weight,
        "type": user.user_type,
        "no_meals": user.no_meals,
        "cuisine_type": user.cuisine_type,
        "activity_level": user.activity_level,
        "end_goal": user.end_goal
    }

    return jsonify(user_attributes), 200