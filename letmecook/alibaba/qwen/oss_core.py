import os

import oss2
from oss2.credentials import EnvironmentVariableCredentialsProvider

from PIL import Image
from io import BytesIO
import base64


class OSS:
    def __init__(self):
        self.auth = oss2.ProviderAuth(EnvironmentVariableCredentialsProvider())
        self.bucket = oss2.Bucket(self.auth, 'oss-ap-southeast-1.aliyuncs.com', 'qwen-inputs')

    def put_image(self, base64_image):
        im = Image.open(BytesIO(base64.b64decode(base64_image)))

        temp_name = 'image_to_analyze.png'

        im.save(temp_name, 'PNG')

        self.bucket.put_object_from_file(temp_name, temp_name)
