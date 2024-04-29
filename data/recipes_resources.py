from flask import jsonify
from flask_restful import reqparse, Resource, abort
from data import db_session
from data.cats import Cat
from data.rec_cats import RecCat
from data.recipes import Recipe

parser = reqparse.RequestParser()
parser.add_argument('name', required=True)
parser.add_argument('ingredients', required=True)
parser.add_argument('recipe', required=True, type=int)


def abort_if_recipe_not_found(recipe_id):
    session = db_session.create_session()
    recipe = session.query(Recipe).get(recipe_id)
    if not recipe:
        abort(404, message=f"Recipe {recipe_id} not found")


class RecipeListResource(Resource):
    def get(self):
        session = db_session.create_session()
        recipe = session.query(Recipe).all()
        return jsonify({'recipe': [item.to_dict(only=('id', 'name', 'ingredients')) for item in recipe]})


class ListCategory(Resource):
    def get(self, ):
        session = db_session.create_session()
        category = session.query(Cat).all()
        return jsonify({'category': [item.to_dict(
            only=('id', 'name')) for item in category]})


class RecipeListCategory(Resource):
    def get(self, category_id):
        session = db_session.create_session()
        temp = [el.id for el in session.query(RecCat).filter(RecCat.id_cats == category_id).all()]
        recipe = session.query(Recipe).filter(Recipe.id.in_(temp)).all()
        return jsonify({'recipe': [item.to_dict(
            only=('id', 'name', 'ingredients')) for item in recipe]})


class RecipeResource(Resource):
    def get(self, recipe_id):
        abort_if_recipe_not_found(recipe_id)
        session = db_session.create_session()
        recipe = session.query(Recipe).get(recipe_id)
        return jsonify({'recipe': recipe.to_dict(
            only=('name', 'ingredients', 'recipe'))})

    def delete(self, recipe_id):
        abort_if_recipe_not_found(recipe_id)
        session = db_session.create_session()
        recipe = session.query(Recipe).get(recipe_id)
        session.delete(recipe)
        session.commit()
        return jsonify({'success': 'OK'})

    def put(self, recipe_id):
        abort_if_recipe_not_found(recipe_id)
        args = parser.parse_args()
        session = db_session.create_session()
        recipe = session.query(Recipe).get(recipe_id)
        recipe.name = args['name']
        recipe.ingredients = args['ingredients']
        recipe.recipe = args['recipe']
        session.commit()
        return jsonify({'success': 'OK'})
