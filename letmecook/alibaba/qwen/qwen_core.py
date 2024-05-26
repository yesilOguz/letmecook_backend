from letmecook.alibaba.qwen import tokenizer, model


class Qwen:
    def __init__(self):
        self.text = 'You are an assistant that only gives json with the structure {"ingredients": [ingredient1, ingredient2]}. what are the ingeridents in the food?'

    def prompt(self, image_url):
        query = tokenizer.from_list_format([
            {'image': image_url},
            {'text': 'You are an assistant that only gives json with the structure {"ingredients": [ingredient1, ingredient2]}. what are the ingeridents in the food?'},
        ])

        response, history = model.chat(tokenizer, query=query, history=None)
        return response
