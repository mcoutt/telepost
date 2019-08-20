import os, sys
import string, random
import datetime

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
# os.environ['DJANGO_SETTINGS_MODULE'] = 'teleblog.settings'
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "teleblog.settings")

import django

django.setup()

from django.contrib.auth.models import User, Group
from django.db import connection


def sql_del_permissions():
    with connection.cursor() as cursor:
        sql = "DELETE {} FROM {};".format("", "auth_group_permissions",)
        cursor.execute(sql)
        cursor.close()


def sql_del_users():
    with connection.cursor() as cursor:
        sql = "DELETE {} FROM {};".format("", "auth_user",)
        cursor.execute(sql)
        cursor.close()


def sql_del_groups():
    with connection.cursor() as cursor:
        sql = "DELETE {} FROM {};".format("", "auth_group",)
        cursor.execute(sql)
        cursor.close()


def clear():

    Group.objects.all().delete()

    sql_del_permissions()
    sql_del_groups()
    User.objects.all().delete()
    # sql_del_users()

    # Permission.objects.all().delete()

    print("complete... ")


if __name__ == '__main__':
    print("Start clearing script...")
    clear()
