from django.urls import path
from . import views


urlpatterns = [
    path('', views.UserList.as_view(), name='index'),
    path('create/', views.Login.as_view()),
    path('update/', views.UserRetrieveUpdateAPIView.as_view()),
]
