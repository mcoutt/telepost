import clearbit
from teleblog import settings
from .models import ClearbitUser
from pymongo import MongoClient

clearbit.key = settings.clearbit_key

connection = MongoClient(
            settings.mongo_db_server,
            settings.mongo_db_port,
            username=settings.mongo_db_user,
            password=settings.mongo_db_pwd,
            authSource=settings.mongo_db_auth,
        )
db = connection[settings.mongo_db_name]
clearbit_data = db['clearbit_data']


def get_clearbit_data(_email):
    res = clearbit.Enrichment.find(email=_email, stream=True)
    # ClearbitUser.objects(email=_email, data=res).save()
    return {'status': 'ok', 'data': res}
