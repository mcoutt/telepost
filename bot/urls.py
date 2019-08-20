from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from . import views

app_name = 'bot'


urlpatterns = [
    path('', views.UpdateBot.as_view(), name='update'),
]
