from django.urls import path

from . import views

app_name = 'bot'

urlpatterns = [
    path('menu/', views.bot_menu, name='menu'),
    path('reglas/', views.bot_reglas, name='reglas'),
    path('test/', views.bot_test, name='test'),
    path('test/bot_responde/', views.bot_responde, name='bot_responde'),
]