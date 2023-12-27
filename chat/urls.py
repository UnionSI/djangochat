from django.urls import path

from . import views, webhooks

app_name = 'room'

urlpatterns = [
    path('chats/', views.chats, name='chats'),
    path('chat/<int:id>/', views.chat, name='chat'),
    path('chats-dev/', views.chats, name='chats-dev'),
    path('chat-dev/<int:id>/', views.chat, name='chat-dev'),
    path('embudos/', views.embudos, name='embudos'),
    path('embudo/<int:id>/', views.embudo, name='embudo'),
    path('mover_de_sector/<int:room_id>/<int:sector_tarea_id>/', views.mover_de_sector, name='mover_de_sector'),
    path('green_api_webhook/', webhooks.green_api_webhook, name='green_api_webhook'),
    path('waapi_api_webhook/', webhooks.waapi_api_webhook, name='waapi_api_webhook'),
]