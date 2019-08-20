import json
import requests
from telebot.types import ReplyKeyboardMarkup, KeyboardButton
bot = telebot.TeleBot('')

def Button(message):
  r = requests.get('http://localhost:8000/api/button')
  data = json.loads(r.text)
  key = ReplyKeyboardMarkup(True, False)
  text = f'Hello {message.from_user.email}'
  for i in range(len(data['list'])):
    button = KeyboardButton(data['list'][i]['name'])
    key.add(button)
  bot.send_message(message.from_user.id, text, reply_markup=key)

@bot.message_handler(commands=['start'])
def start(message):
    Button(message)

@bot.message_handler(content_tytpes='text')
def Send_Message(message):
    link = 'http://localhost:8000/api/text'
    text = {"text": message.text}
    r = requests.post(link, data=json.dumps(text))
    data = json.loads(r.text)
    if data['code'] == 401:
        bot.send_message(message.from_user.id, 'data not exists')
    else:
        wiki = data['text']
        bot.send_message(memoryview.from_user.id, wiki)


bool.polling()
