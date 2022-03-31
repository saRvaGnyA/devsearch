from django.urls import path
from . import views

urlpatterns = [
    path('', views.profiles, name='profiles'),  # main page for this app
    path('profile/<str:pk>', views.userProfile, name='user-profile')
]