from letmecook.alibaba.qwen.models import QwenDetectModel
from letmecook.core.mongo_database import DB
from letmecook.recipe.validator import validate_object_id
from letmecook.user.models import UserDBModel
from letmecook.user.routes import collection_name
from fastapi import APIRouter, status, HTTPException, Body

from letmecook.alibaba.qwen.qwen_core import Qwen
from letmecook.alibaba.qwen.oss_core import OSS

router = APIRouter()


@router.post('/detect', status_code=status.HTTP_200_OK)
def detect(image_model: QwenDetectModel = Body(...)):
    oss_object = OSS()
    qwen = Qwen()

    image_name = oss_object.put_image(image_model.base64_image)

    response = qwen.prompt('https://qwen-inputs.oss-ap-southeast-1.aliyuncs.com/image_to_analyze.png')

    return response
