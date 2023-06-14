from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Prefetch

from .models import Room, Message

@login_required
def chats(request):
    rooms = Room.objects.prefetch_related(
        Prefetch('messages', queryset=Message.objects.order_by('-date_added')[:1], to_attr='last_message')
    )
    return render(request, 'room/chats.html', {'rooms': rooms})

@login_required
def rooms(request):
    rooms = Room.objects.all()
    return render(request, 'room/rooms.html', {'rooms': rooms})

@login_required
def chat(request, slug):
    room = Room.objects.get(slug=slug)
    messages = Message.objects.filter(room=room)[0:25]
    rooms = Room.objects.prefetch_related(
        Prefetch('messages', queryset=Message.objects.order_by('-date_added')[:1], to_attr='last_message')
    )
    return render(request, 'room/chats.html', {'room': room, 'chat_messages': messages, 'rooms': rooms,})