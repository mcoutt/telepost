import time
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from django.http import HttpResponse
from post.models import Post
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import telebot
import json
from telebot import types
from user.auth import login
from user.models import User
from teleblog import settings
from social.views import get_clearbit_data, get_emailhunter_data
from pymongo import MongoClient

client = MongoClient()
db = client[settings.mongo_db_name]
mongo_users = db['users']
bot = telebot.TeleBot(settings.tel_key)
result_getting_info = {}
user_dict = {}
post_dict = {}
like_symbol = '👍'
unlike_symbol = '👎'


class UpdateBot(APIView):
    """ Start of bot work in django connections with next (start) handler run """
    permission_classes = (AllowAny,)

    def get(self, request, *args, **kwargs):
        return HttpResponse("bot is running...")

    def post(self, request):
        json_string = request.body.decode("UTF-8")
        update = telebot.types.Update.de_json(json_string)
        bot.process_new_updates([update])

        return Response({'code': 200})


@bot.message_handler(commands=['start'])
def send_welcome(message):
    get_user = message.from_user.id
    user = User.objects.filter(telegram_id=get_user).first()
    if not user:
        msg = bot.reply_to(message, "Hi there.. You need SingUp. Please tape your email.")
        bot.register_next_step_handler(msg, process_email_handler)
    else:
        msg = bot.reply_to(message, f"Hi there, {user} !")
        bot.register_next_step_handler(msg, process_post_handler(message))


@bot.message_handler(commands=['help'])
def send_welcome(message):
    chat_id = message.chat.id
    get_user = message.from_user.id
    user = User.objects.filter(telegram_id=get_user).first()
    if not user:
        bot.send_message(chat_id, "Hi there.. You need SingUp. Please tape /start.")
    else:
        bot.send_message(chat_id, "You can get all posts with the View button or create the new post "
                                  "with the Create button ")


def process_email_handler(message):
    """ Get need data of user and save it to sql and mongo """
    try:
        if message.text:
            user_dict['email'] = message.text
            clearbit_data = get_clearbit_data(user_dict['email'])
            emailhunter_data = get_emailhunter_data(user_dict['email'])
            result_getting_info['clearbit'] = clearbit_data.get('data')
            result_getting_info['emailhunter'] = emailhunter_data.get('data')
            mongo_users.insert_one(result_getting_info)
            if user_dict.get('email'):
                msg = bot.reply_to(message, "Please tape your first name, last name and password with space separate")
                bot.register_next_step_handler(msg, process_signup_step)
    except Exception as e:
        bot.reply_to(message, f'process_email_handler error: {e}')


def process_signup_step(message):
    """ Get data for registered user """
    try:
        chat_id = message.chat.id
        if message.text:
            full_name = str(message.text).split(' ')
            if full_name.__len__() == 3:
                user_dict['fname'] = full_name[0]
                user_dict['lname'] = full_name[1]
                user_dict['telegram_id'] = message.from_user.id
                user_dict['telegram_chat_id'] = chat_id
                user = User.objects.create(**user_dict)
                user.token = login(user)
                user.set_password(full_name[2])
                user.save()
                msg = bot.reply_to(message, 'Welcome..')
                bot.register_next_step_handler(msg, process_post_handler)
            else:
                bot.send_message(chat_id, text=f"full info is not exists..")
    except Exception as e:
        bot.reply_to(message, f'oos: {e}')


def process_post_handler(message):
    """ View all posts with the add keyboard after login registered user """
    try:
        chat_id = message.chat.id
        posts(chat_id)
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        markup.add('Add post', 'View Posts')
    except Exception as e:
        bot.reply_to(message, f'process_post_handler error: {e}')


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    """ Add like or unlike with check of count max likes per user"""
    if call.message:
        chat_id = call.message.chat.id
        user = call.message.from_user.id
        user_count_likes = User.objects.filter(telegram_id=user).first()
        if user_count_likes.max_like <= settings.max_likes_per_user:
            work = call.data.split('_')
            if 'like' == work[0]:
                post_id = work[1]
                post = Post.objects.get(id=post_id)
                post.like = post.like + 1
                post.save()
            elif 'unlike' == work[0]:
                post_id = work[1]
                post = Post.objects.get(id=post_id)
                post.unlike = post.unlike + 1
                post.save()
        else:
            bot.send_message(chat_id, text=f"You count of likes more then limit..")


def posts(chat_id):
    """ Get from DB all posts and render it """
    posts = Post.objects.all()
    for i in posts:
        keyboard = InlineKeyboardMarkup()
        first_btn = InlineKeyboardButton(text=f'{like_symbol} {i.like}', callback_data=f'like_{i.id}')
        second_btn = InlineKeyboardButton(text=f'{unlike_symbol} {i.unlike}', callback_data=f'unlike_{i.id}')
        keyboard.add(first_btn, second_btn)
        bot.send_message(chat_id, text=f"{i.title} \n{i.description}", reply_markup=keyboard)


@bot.message_handler(func=lambda message: message.text == "Add post")
def command_text_handler(m):
    """ Run event for save a new post """
    chat_id = m.chat.id
    user = m.from_user.id
    user_count_posts = User.objects.filter(telegram_id=user).first()
    if user_count_posts.max_post <= settings.max_post_per_user:
        msg = bot.reply_to(m, "Add title:")
        bot.register_next_step_handler(msg, process_create_title_post_handler)
    else:
        bot.send_message(chat_id, text=f"You count of posts more then limit..")


@bot.message_handler(func=lambda message: message.text == "View")
def command_text_handler(m):
    """ Get all posts with View button """
    chat_id = m.chat.id
    posts(chat_id)


def process_create_title_post_handler(message):
    """ Get and temporary save title of post and redirect to next handler """
    try:
        chat_id = message.chat.id
        if message.text:
            post_dict['title'] = message.text
            msg = bot.reply_to(message, 'Add post content..')
            bot.register_next_step_handler(msg, process_create_post_handler)
        else:
            bot.send_message(chat_id, text=f"full info is not exists..")
    except Exception as e:
        bot.reply_to(message, f'oos: {e}')


def process_create_post_handler(message):
    """ Save new post with add one to total posts per user to user model """
    try:
        chat_id = message.chat.id
        if message.text:
            post_dict['description'] = message.text
            post = Post.objects.create(**post_dict)
            post.save()
            user = User.objects.get(id=message.from_user.id)
            user.max_post = user.max_post + 1
            user.save()
            msg = bot.reply_to(message, 'Post added..')
            bot.register_next_step_handler(msg, process_post_handler)
        else:
            bot.send_message(chat_id, text=f"full info is not exists..")
    except Exception as e:
        bot.reply_to(message, f'oos: {e}')


bot.enable_save_next_step_handlers(delay=0)
bot.load_next_step_handlers()
