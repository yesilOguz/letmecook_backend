import requests
import time
import hmac
import hashlib
import base64
from letmecook.alibaba.core import ACCESS_KEY_ID, ACCESS_KEY_SECRET

class Translate:
    def __init__(self):
        # Şuan test etmk korkutucu zaten para kesebiliyore ( Probabaly )
        self.api_url = 'http://mt.cn-hangzhou.aliyuncs.com/api/translate/web/general'

    # Çalışmayacak çünkü api keyleri envayrımınt a vermedik heheh
    def translate(self, source_lang, target_lang, text):
        json_data = {'FormatType': 'text',
                     'SourceLanguage': source_lang,
                     'TargetLanguage': target_lang,
                     'SourceText': text,
                     'Scene': 'title'}

        timestamp = int(round(time.time() * 1000))

        string_to_sign = f"POST\n{'/'}\n\n{timestamp}\nacs={ACCESS_KEY_ID}"

        hashed_data = hmac.new(
            ACCESS_KEY_SECRET.encode('utf-8'),
            string_to_sign.encode('utf-8'),
            hashlib.sha1
        ).digest()

        signature = base64.b64encode(hashed_data).decode('utf-8')

        parameters = {
            "Timestamp": timestamp,
            "Signature": signature,
            "AccessKeyId": ACCESS_KEY_ID,
            **json_data
        }

        response = requests.post(self.api_url, json=json_data, params=parameters)

        return response
