from django.urls import path

from . import views


urlpatterns = [
    path('', views.PostAPIView.as_view()),
    path('<pk>/', views.PostAPIView.as_view()),
    path('like/<pk>/', views.PostLikesAPIView.as_view()),
    path('unlike/<pk>/', views.PostUnlikesAPIView.as_view()),
]
