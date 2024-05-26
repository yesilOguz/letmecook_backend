import random

from faker import Faker
import pytest
from fastapi.testclient import TestClient

from letmecook.user.models import UserCreateModel, UserDBModel
from letmecook.user.routes import collection_name
from main import app
from letmecook.core.mongo_database import MONGO, DB

Faker.seed()
faker = Faker()
@pytest.fixture(scope="function")
def test_client():
    with TestClient(app) as client:
        yield client
        MONGO.drop_database()

@pytest.fixture()
def user_db_factory():
    user = UserCreateModel(name=faker.name(), username=faker.user_name(), password=faker.word())
    inserted = DB[collection_name].insert_one(user.to_mongo())
    created_user = DB[collection_name].find_one({"_id": inserted.inserted_id})
    return UserDBModel.from_mongo(created_user)

@pytest.fixture()
def recipe_id_factory():
    return random.choice([602638, 1088123, 487873, 1091174])
