import os
import requests
from random import sample
from bson import ObjectId

from letmecook.core.mongo_database import DB
from letmecook.recipe.validator import validate_object_id
from letmecook.user.models import UserDBModel
from letmecook.user.routes import collection_name
from fastapi import APIRouter, status, HTTPException
from letmecook.recipe.models import Recipe, SingleSimilarRecipe, SimilarRecipe, RecipeInformation, SearchRecipeResponse, RecipeRandomResponse

router = APIRouter()
headers = {
    "X-RapidAPI-Key": os.getenv("RAPID_API_KEY"),
    "X-RapidAPI-Host": "spoonacular-recipe-food-nutrition-v1.p.rapidapi.com"
}
api_url = "https://spoonacular-recipe-food-nutrition-v1.p.rapidapi.com/recipes/"


@router.get("/search/{ingredients}", status_code=status.HTTP_200_OK, response_model=dict)
def search_ingredient(ingredients):
    if ingredients.strip() == "":
        raise HTTPException(status.HTTP_400_BAD_REQUEST,
                            detail='içerikler boş gönderilemez.')

    search_url = api_url + "findByIngredients"

    json_data = {"ingredients": ingredients, "number": 5}
    response = requests.get(search_url, headers=headers, params=json_data)

    recipies = []
    for recipe in response.json(): # bu jsondan gelen bir keyin içerisine bakacak olabilirsin şuan kontrol edemiyorum ( train deyim )
        found_recipe = Recipe.from_json(recipe)

        if found_recipe.id is None:
            continue

        recipies.append(found_recipe)

    return recipies


@router.get("/get-random", status_code=status.HTTP_200_OK, response_model=dict)
def get_random():
    random_url = api_url + "random"
    type_of_food = ["vegetarian", "vegan", "gluten free", "dairy free", "low fodmap",
                    "french", "chinese", "italian", "mexican", "japanese"]

    random_type_of_foods = sample(type_of_food, 3)
    result = {}

    for random_of_food in random_type_of_foods:
        params = {
            "number": 3,
            "tags": random_of_food
        }
        response = requests.get(random_url, params=params, headers=headers)
        
        recipes = []
        for recipe in response.json()['recipes']:
            recipes.append(RecipeRandomResponse.from_json(recipe)) 

        result[random_of_food] = recipes

    return {'result': result, 'categories': random_type_of_foods}


@router.get("/favorite/{recipe_id}/{user_id}", status_code=status.HTTP_200_OK, response_model=bool)
@validate_object_id('user_id')
def add_favorite(recipe_id, user_id):
    result = DB[collection_name].find_one({"_id": ObjectId(user_id)})
    result = UserDBModel.from_mongo(result)

    if not result:
        raise HTTPException(status.HTTP_400_BAD_REQUEST,
                            detail='kullanıcı bulunamadı.')

    if int(recipe_id) in result.recipies_like:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail="Bu tarif favorilere eklenmiş.")

    result.recipies_like.append(recipe_id)
    DB[collection_name].find_one_and_update(filter={"_id": result.id},
                                            update={"$set": result.to_mongo(exclude_unset=False)})
    return True


@router.get("/delete-favorite/{recipe_id}/{user_id}", status_code=status.HTTP_200_OK, response_model=bool)
@validate_object_id('user_id')
def delete_favorite(recipe_id, user_id):
    result = DB[collection_name].find_one({"_id": ObjectId(user_id)})
    result = UserDBModel.from_mongo(result)

    if not result:
        raise HTTPException(status.HTTP_400_BAD_REQUEST,
                            detail='Kullanıcı bulunamadı.')

    if int(recipe_id) not in result.recipies_like:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail="Bu tarif favorilerde değil.")

    result.recipies_like.remove(int(recipe_id))
    DB[collection_name].find_one_and_update(filter={"_id": result.id}, update={"$set": result.to_mongo()})

    return True


@router.get("/get-favorite/{user_id}", status_code=status.HTTP_200_OK)
@validate_object_id('user_id')
def get_favorite(user_id):
    result = DB[collection_name].find_one({"_id": ObjectId(user_id)})
    result = UserDBModel.from_mongo(result)

    if not result:
        raise HTTPException(status.HTTP_400_BAD_REQUEST,
                            detail='kullanıcı bulunamadı!')

    return result.recipies_like


@router.get("/get-favorite-by-username/{username}", status_code=status.HTTP_200_OK)
def get_favorite_by_username(username):
    result = DB[collection_name].find_one({"username": username})
    result = UserDBModel.from_mongo(result)

    if not result:
        raise HTTPException(status.HTTP_404_NOT_FOUND,
                            detail='kullanıcı bulunamadı!')

    return result.recipies_like


@router.get("/get-recipe/{recipe_id}", status_code=status.HTTP_200_OK, response_model=RecipeInformation)
def get_recipe(recipe_id):
    if recipe_id.strip() == "":
        raise HTTPException(status.HTTP_400_BAD_REQUEST,
                            detail='tarif id değeri boş gönderilemez!')

    recipe_url = api_url + f"{recipe_id}/information"
    similar_url = api_url + f"{recipe_id}/similar"
    recipe_response = requests.get(recipe_url, headers=headers)
    similar_response = requests.get(similar_url, headers=headers)

    if recipe_response.status_code == 404 or similar_response.status_code == 404:
        raise HTTPException(status.HTTP_400_BAD_REQUEST,
                            detail='Geçersiz id girdiniz')

    recipes = [SingleSimilarRecipe.from_json(similar_recipe) for similar_recipe in similar_response.json()]
    similar = SimilarRecipe(recipes=recipes)

    recipe = RecipeInformation.from_json(recipe_response.json())
    recipe.similar = similar
    return recipe


@router.get("/search-recipe/{recipe_name}", status_code=status.HTTP_200_OK, response_model=SearchRecipeResponse)
def search_recipe(recipe_name):
    if recipe_name.strip() == "":
        raise HTTPException(status.HTTP_400_BAD_REQUEST,
                            detail='tarif ismi boş gönderilemez.')

    search_recipe_url = api_url + "complexSearch"
    params = {"query": recipe_name}
    response = requests.get(search_recipe_url, params=params, headers=headers)
    return SearchRecipeResponse.from_json(response.json())
