from mongoengine import *


class ClearbitUser(Document):
    email = StringField(max_length=200)
    data = StringField(max_length=200)


class EmailhunterUser(Document):
    email = StringField(max_length=200)
    data = StringField(max_length=200)
