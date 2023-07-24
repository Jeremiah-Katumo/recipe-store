from flask import request, jsonify,make_response
from flask_restx import Namespace, Resource, fields
from models import Recipe
from flask_jwt_extended import jwt_required 


recipe_ns = Namespace('recipe', description='A namespace for Recipes')

# generate access token
access_token = Recipe

# Create a model (serializer) to serialize the model into json file
recipe_model = recipe_ns.model(
    "Recipe",
    {
        "id":fields.Integer(),
        "title":fields.String(),
        "description":fields.String()
    }
)


# The class in thisroute defines all the methods that will be used by the route
@recipe_ns.route('/hello')
class HelloResource(Resource):
    def get(self):
        return {"message":"Hello World!"}
    

@recipe_ns.route('/recipes')
class RecipesResource(Resource):

    @recipe_ns.marshal_list_with(recipe_model)
    def get(self):
        """Get all recipes """
        
        recipes = Recipe.query.all()        # Turn it to a json file using the serializer, api.marshal_list_with(recipe_model)
        
        return recipes

    @recipe_ns.marshal_with(recipe_model)
    @recipe_ns.expect(recipe_model)
    @jwt_required()
    def post(self):
        """Create a new recipe"""

        data = request.get_json()

        # Create a new recipe
        new_recipe = Recipe(
            title = data.get('title'),
            description = data.get('description')
        )

        # generate access token
        # access_token = new_recipe.encode_auth_token(new_recipe.id)
        # response_object = {
        #     'title': 'Test Chapati',
        #     'description': 'Test chapati description',
        #     'access_token': access_token.decode()
        # }

        new_recipe.save()

        return new_recipe, 201
        # return make_response(jsonify(response_object)), 201


@recipe_ns.route('/recipe/<int:id>')
class RecipeResource(Resource):

    @recipe_ns.marshal_with(recipe_model)
    def get(self, id):
        """Get recipe by id """

        # Get recipe by id
        recipe = Recipe.query.get_or_404(id)

        return recipe

    @recipe_ns.marshal_with(recipe_model)
    @recipe_ns.expect(recipe_model)
    @jwt_required()                   # protect the route for updating
    def put(self, id):
        """Update a recipe by id """

        # Get the recipe by id if it exists else return error 404
        recipe_to_update = Recipe.query.get_or_404(id)

        # Get the data of the recipe to update
        data = request.get_json()

        # Then update the recipe using the update method in Recipe class (models.py)
        recipe_to_update.update(data.get('title'), data.get('description'))   # Pass the title and description is obtained from the update method of the Recipe classin models.py

        return recipe_to_update

    @recipe_ns.marshal_with(recipe_model)
    @jwt_required()
    def delete(self, id):
        """Delete a recipe by id"""

        recipe_to_delete = Recipe.query.get_or_404(id)

        recipe_to_delete.delete()
        
        return recipe_to_delete
