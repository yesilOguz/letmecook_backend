import pytest
import random

from bson import ObjectId
from faker import Faker

from letmecook.core.mongo_database import DB
from letmecook.user.models import UserDBModel
from letmecook.user.routes import collection_name

Faker.seed(3)
faker = Faker()


@pytest.fixture()
def ingredients_name_factory():
    return "tomatoes,potatoes,milk,salami,ham"


@pytest.fixture()
def recipe_name_factory():
    recipe_name = ["turkish pizza", "sushi", "mac and cheese", "lasagna", "pie", "moussaka"]
    recipe_name = random.choice(recipe_name)
    return recipe_name


@pytest.fixture()
def favorite_recipe_db_factory():
    def _func(user_id: ObjectId, count=1):
        user_collection = DB[collection_name].find_one({'_id': user_id})
        user = UserDBModel.from_mongo(user_collection)
        for i in range(count):
            user.recipies_like.append(i)

        DB[collection_name].find_one_and_update(filter={"_id": user.id},
                                                update={"$set": user.to_mongo(exclude_unset=False)})
    return _func

