from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Prefetch
from django.db.models import Max, Subquery, OuterRef

from .models import Sector, SectorTarea, Room, Message

@login_required
def chats(request):
    rooms = Room.objects.prefetch_related(
        Prefetch('messages', queryset=Message.objects.order_by('-fecha_hora')[:1], to_attr='last_message')
    )
    return render(request, 'room/chats.html', {'rooms': rooms})


@login_required
def chat(request, slug):
    room = get_object_or_404(Room, slug=slug)
    messages = Message.objects.filter(contacto=room)[0:25]
    rooms = Room.objects.prefetch_related(
        Prefetch('messages', queryset=Message.objects.order_by('-fecha_hora')[:1], to_attr='last_message')
    )
    return render(request, 'room/chats.html', {'room': room, 'chat_messages': messages, 'rooms': rooms,})


@login_required
def embudos(request):
    embudos = Sector.objects.all()
    return render(request, 'room/embudos.html', {'embudos': embudos})


@login_required
def embudo(request, id):
    sector = get_object_or_404(Sector, id=id)
    sectores = Sector.objects.all()
    sector_tareas = SectorTarea.objects.filter(sector=sector)
    rooms = Room.objects.filter(messages__sector_tarea__sector=sector).distinct()

    objeto_rooms = {}
    for room in rooms:
        ultimo_mensaje = Message.objects.filter(contacto=room).order_by('-fecha_hora')[:1]
        objeto_rooms[room] = ultimo_mensaje

    objeto_sector_tareas = {}
    for sector_tarea in sector_tareas:
        objeto_sector_tareas[sector_tarea] = []
        for room, mensaje in objeto_rooms.items():
            if mensaje[0].sector_tarea == sector_tarea:
                objeto_sector_tareas[sector_tarea].append([room, mensaje])    

    return render(request, 'room/embudos.html', {'embudo': sector, 'embudos': sectores, 'sector_tareas':objeto_sector_tareas})
    

    '''
    # Obtener todas las sector_tareas que pertenecen al embudo actual
    sector_tareas = SectorTarea.objects.filter(sector=embudo)
    # Crear una consulta Prefetch para cargar las rooms relacionadas con las sector_tareas
    rooms_prefetch = Prefetch(
        'room_set',
        queryset=Room.objects.prefetch_related(
            Prefetch('messages', queryset=Message.objects.order_by('-fecha_hora')[:1], to_attr='last_message')
        ),
        to_attr='rooms'
    )
    sector_tareas = sector_tareas.prefetch_related(rooms_prefetch)
    '''