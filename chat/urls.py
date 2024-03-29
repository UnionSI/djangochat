from django.urls import path

from . import views, webhooks

app_name = 'contacto'

urlpatterns = [
    path('chat/todos', views.chats, name='chats'),
    path('chat/<int:id>/', views.chat, name='chat'),
    path('chat-dev/todos', views.chats, name='chats-dev'),
    path('chat-dev/<int:id>/', views.chat, name='chat-dev'),
    path('embudo/todos', views.embudos, name='embudos'),
    path('embudo/<int:id>/', views.embudo, name='embudo'),
    path('mover_de_sector/<int:contacto_id>/<int:sector_tarea_id>/', views.mover_de_sector, name='mover_de_sector'),
    #path('green_api_webhook/', webhooks.green_api_webhook, name='green_api_webhook'),
    path('waapi_api_webhook/', webhooks.waapi_api_webhook, name='waapi_api_webhook'),
    path('chat/<int:id>/cargar-mas-mensajes/<int:page>/', views.cargar_mas_mensajes, name='cargar_mas_mensajes'),
]