import instabot
from flask import Flask, request, json

app = Flask(__name__)

@app.route('/', methods=['POST'])


def processing():
    #Распаковываем json из пришедшего POST-запроса
    data = json.loads(request.data)
    #Вконтакте в своих запросах всегда отправляет поле типа
    if 'type' not in data.keys():
        return 'not vk'
    if data['type'] == 'confirmation':
        return '7dee3274'
    elif data['type'] == 'message_new':
        print(list(data['object']))
        chat.create_answer(data['object'])
        return 'ok'
def hello_world():
    return 'Hello from Flask!'
