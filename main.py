from fastapi import APIRouter, status, FastAPI
from contextlib import asynccontextmanager

from letmecook.core.mongo_database import MONGO
from letmecook.user.routes import router as user_router
from letmecook.recipe.routes import router as recipe_router
from letmecook.alibaba.qwen.routes import router as qwen_router


router = APIRouter()


@router.get('/', status_code=status.HTTP_200_OK)
def main_path():
    return {'LetMeCook!': 'v1.0'}


@asynccontextmanager
async def lifespan(app: FastAPI):
    if not MONGO.check_connection():
        MONGO.reconnect()

    app.database = MONGO.get_db()

    yield

    MONGO.shut_down_db()

app = FastAPI(lifespan=lifespan)

app.include_router(router)
app.include_router(user_router, prefix="/user")
app.include_router(recipe_router, prefix='/recipe')
app.include_router(qwen_router, prefix='/qwen')
