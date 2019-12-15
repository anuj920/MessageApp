from django.conf.urls import url
from normal import views


urlpatterns = [
    url(r'^$',views.OwnMessageList.as_view(),name='message_list'),
    url(r'^ownmessage$',views.OwnMessageList.as_view(),name='own_message_list'),
    url(r'^message/(?P<pk>\d+)$', views.MessageDetailView.as_view(), name='message_detail'),
    url(r'^message/new/$', views.CreateMessageView.as_view(), name='message_new'),
    url(r'^message/(?P<pk>\d+)/edit/$', views.MessageUpdateView.as_view(), name='message_edit'),
    url(r'^message/(?P<pk>\d+)/remove/$', views.MessageDeleteView.as_view(), name='message_remove'),
]