from marshmallow import Schema
from marshmallow import fields


class PlainFavSchema(Schema):
    fav_id= fields.Int(dump_only=True)
    dish=fields.Str()
    calories=fields.Int()
    carbs=fields.Int()
    protein=fields.Int()
    fat=fields.Int()
    image_url=fields.URL()


class PlainRecipeSchema(Schema):
    id = fields.Int(dump_only=True)
    title= fields.Str()
    

class PlainDietSchema(Schema):
    id = fields.Int(dump_only=True)
    Calorie = fields.Int(required=True)
    


class PlainUserSchema(Schema):
    id = fields.Int(dump_only=True)
    username = fields.Str()
    email = fields.Str()
    password = fields.Str()
    gender = fields.Str()
    diet_type = fields.Str()
    age = fields.Int()
    height = fields.Int()
    weight = fields.Int()
    user_type = fields.Str()
    allergies = fields.Str()
    no_meals = fields.Int()
    cuisine_type = fields.Str()
    activity_level = fields.Str()
    end_goal = fields.Str()
    calorie=fields.Str()
    carbs = fields.Str()
    protein =  fields.Str()
    fats =  fields.Str() 
    timestamp = fields.DateTime()


class FavSchema(PlainFavSchema):
    user_id = fields.Int(required=True, load_only=True)
    user = fields.Nested(PlainUserSchema(), dump_only=True)

class RecipeSchema(PlainRecipeSchema):
    diet_id = fields.Int(required=True, load_only=True)
    diet = fields.Nested(PlainDietSchema(), dump_only=True)

class DietSchema(PlainDietSchema):
    user_id = fields.Int(required=True, load_only=True)
    user = fields.Nested(PlainUserSchema(), dump_only=True)
    meals = fields.List(fields.Nested(PlainRecipeSchema()), dump_only=True)


class UserSchema(PlainUserSchema):
    dietplan = fields.List(fields.Nested(PlainDietSchema()), dump_only=True)
    fav=fields.List(fields.Nested(PlainFavSchema()),dump_only=True)