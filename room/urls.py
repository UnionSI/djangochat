from django.urls import path

from . import views

app_name = 'room'

urlpatterns = [
    path('', views.rooms, name='rooms'),
    path('chats/', views.chats, name='chats'),
    path('chat/<slug:slug>/', views.chat, name='chat'),
]