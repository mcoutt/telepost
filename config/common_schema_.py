import os
import sys
import string
import random
import datetime

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
# os.environ['DJANGO_SETTINGS_MODULE'] = 'teleblog.settings'
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "teleblog.settings")

from django.core.files import File
import django
django.setup()

from django.contrib.auth.models import User, Group
from django.contrib.auth import get_user_model
from django.db import connection
base_path = "teleblog/site_content/images"


def id_generator(size=14, chars=string.ascii_letters + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def number_generator(size=14, chars=string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


if __name__ == '__main__':
    print("Starting common schema script...")
    print("Ok, done...")
