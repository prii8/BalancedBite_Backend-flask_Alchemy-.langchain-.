import asyncio
import os
from flask import Flask, app,jsonify
from flask_sqlalchemy import SQLAlchemy
from pkg_resources import load_entry_point
from flask_smorest import Api
from flask_cors import CORS,cross_origin
from sqlalchemy import create_engine
from resources.diet import blp as DietBlueprint
from resources.user import blp as UserBlueprint
from resources.test import blp as TestBlueprint
from resources.Auth import auth_bp
from resources.langchain import blp as LangBlueprint, fetch_recipe_information
from resources.recipe import blp as RecipeBlueprint
from resources.favourite import blp as FavBlueprint
from resources.Breaku import blp as BreakUBlueprint
from resources.userlog import userl
import logging



from db import db

def create_app(db_url=None):
    app = Flask(__name__)
   
   
    app.config["PROPAGATE_EXCEPTIONS"] = True
    app.config["API_TITLE"] = "BALANCED BITE"
    app.config["API_VERSION"] = "v1"
    app.config["OPENAPI_VERSION"] = "3.0.3"
    app.config["OPENAPI_URL_PREFIX"] = "/"
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
    app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    # app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql://aifitness-user:{os.environ.get('GCP_DB_PASSWORD')}@{os.environ.get('GCP_DB_PRIVATE_IP')}:5432/aifitness"
    app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:postgres@localhost:5432/postgres"

    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)
    api=Api(app)

    log_file = "app.log" 
    logging.basicConfig(level=logging.DEBUG, filename=log_file, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


    with app.app_context():
        db.drop_all()
        db.create_all()
    api.register_blueprint(auth_bp)
    app.register_blueprint(DietBlueprint)
    api.register_blueprint(UserBlueprint)
    api.register_blueprint(TestBlueprint)
    api.register_blueprint(LangBlueprint)
    api.register_blueprint(RecipeBlueprint)
    api.register_blueprint(FavBlueprint)
    api.register_blueprint(userl)
    api.register_blueprint(BreakUBlueprint)
    
    CORS(app,origins='*')
   
    return app

app=create_app()

if __name__ == '__main__':

  app.run()