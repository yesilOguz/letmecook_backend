import pytest
from faker import Faker
from letmecook.user.models import UserCreateModel, UserLoginModel, UserUpdateModel

Faker.seed(3)
faker = Faker()
@pytest.fixture()
def user_create_factory():
    return UserCreateModel(name=faker.name(), username=faker.user_name(), password=faker.word())

@pytest.fixture()
def user_login_factory(user_db_factory):
    user = user_db_factory
    login_user = UserLoginModel(username=user.username, password=user.password)
    return login_user

@pytest.fixture()
def user_update_factory(user_db_factory):
    user = user_db_factory
    update_user = UserUpdateModel(id=user.id, username=faker.user_name(),
                                  password=faker.password(), name=faker.name())
    return update_user

@pytest.fixture()
def user_update_with_params_factory():
    def _func(id, username=faker.user_name(),
              password=faker.password(), name=faker.name()):
        update_user = UserUpdateModel(id=id, username=username,
                                      password=password, name=name)
        return update_user
    return _func


