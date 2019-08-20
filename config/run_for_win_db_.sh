#!/usr/bin/env bash

echo "Start..."

# cd project\ &&
source /Users/hdoc/PycharmProjects/teleblog/venv/bin/activate &&
echo "source ok..."
cd /Users/hdoc/PycharmProjects/teleblog/ &&
python manage.py makemigrations &&
echo "migrations ok..."
python manage.py migrate &&
echo "migrate ok..."

#python manage.py createsuperuser adm &&

#cd config/ &&

#python common_schema_.py &&
#echo "common_schema Ok..."

echo "Done..."
