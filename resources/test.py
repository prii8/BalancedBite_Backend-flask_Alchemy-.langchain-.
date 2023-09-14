from flask import jsonify, request
from flask.views import MethodView
from flask_smorest import Blueprint,abort
import sqlalchemy
from sqlalchemy.exc import SQLAlchemyError,IntegrityError
from db import db
import os



blp = Blueprint("Test", "test", description="Operations to test connection with database")

@blp.route("/test")
class TestConnection(MethodView):
    
    def get(self):
        try:
            db.engine.connect()
            return 'Database connection successful'
        except sqlalchemy.exc.OperationalError as e:
            return 'Database connection failed: ' + str(e)
        
@blp.route("/tables", methods=["GET"])
def get_tables():
    try:
      
        query = sqlalchemy.text("SELECT table_name FROM information_schema.tables WHERE table_type='BASE TABLE' AND table_schema='public'")

       
        with db.engine.connect() as connection:
            result = connection.execute(query)
            table_names = [row[0] for row in result]

        return jsonify({"tables": table_names}), 200

    except Exception as e:
        return jsonify({"message": f"Error getting table names: {e}"}), 500
        

    



