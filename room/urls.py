from django.urls import path

from . import views

app_name = 'room'

urlpatterns = [
    path('chats/', views.chats, name='chats'),
    path('chat/<slug:slug>/', views.chat, name='chat'),
    path('embudos/', views.embudos, name='embudos'),
    path('embudo/<int:id>/', views.embudo, name='embudo'),
    path('mover_de_sector/<int:room_id>/<int:sector_tarea_id>/', views.mover_de_sector, name='mover_de_sector'), 
]