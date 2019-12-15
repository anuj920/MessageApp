from django.urls import path
from accounts import views
from django.conf.urls import url
from django.contrib.auth import views as auth_views



urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('profile/',views.ProfileView.as_view(),name='profile'),
]