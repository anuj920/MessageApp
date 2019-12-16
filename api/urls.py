from django.conf.urls import url
from django.urls import path
from . import views

urlpatterns = [
    # url(r'^api_message$',views.MessageView.as_view(),name='api_message'),
    path("AddMessage/",views.AddMessage.as_view(),name = 'AddMessage'),
    url(r'Message/(?P<pk>[0-9]+)/$', views.MessageOperation.as_view(), name='Message'),
    path("Register/",views.Register.as_view(),name = 'Register'),
    path("Login/",views.Login.as_view(),name = 'Login'),
    path("Logout/",views.Logout.as_view(),name = 'Logout'),
]

