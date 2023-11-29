from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.db.models import Prefetch
from django.db.models import Max, Subquery, OuterRef

from .models import Sector, SectorTarea, Room, Message, ContactoTarea

@login_required
def chats(request):
    rooms = Room.objects.annotate(
        last_message=Subquery(
            Message.objects.filter(contacto=OuterRef('pk')).order_by('-fecha_hora')[:1]
            .values('contenido', 'fecha_hora', 'user__username')
        )
    )
    return render(request, 'room/chats.html', {'rooms': rooms})


@login_required
def chat(request, slug):
    room = get_object_or_404(Room, slug=slug)
    room_messages = Message.objects.filter(contacto=room)  # Ver cómo manejar esto si hay muchos mensajes
    rooms = Room.objects.prefetch_related(
        Prefetch('messages', queryset=Message.objects.order_by('-fecha_hora').first(), to_attr='last_message')
    )
    return render(request, 'room/chats.html', {'room': room, 'chat_messages': room_messages, 'rooms': rooms,})


@login_required
def embudos(request):
    embudos = Sector.objects.all()
    return render(request, 'room/embudos.html', {'embudos': embudos})


@login_required
def embudo(request, id):
    sector = get_object_or_404(Sector, id=id)
    sectores = Sector.objects.prefetch_related('sectortarea_set').all()    
    sector_tareas = SectorTarea.objects.filter(sector=sector).prefetch_related('contactotarea_set__contacto__messages').all()

    '''
    # ¿Mejora la performance si se obtiene el último mensaje en la vista en lugar de pasarle todos los mensajes al template?
    # Agregar el último mensaje a cada Room
    for sector_tarea in sector_tareas:
        for contacto_tarea in sector_tarea.contactotarea_set.all():
            last_message = contacto_tarea.contacto.messages.order_by('-fecha_hora').first()
            contacto_tarea.last_message = last_message
    '''

    return render(request, 'room/embudos.html', {'embudo': sector, 'embudos': sectores, 'sector_tareas': sector_tareas})
    

@login_required
@require_POST
def mover_de_sector(request, room_id, sector_tarea_id):
    room = get_object_or_404(Room, id=room_id)
    sector_tarea = get_object_or_404(SectorTarea, id=sector_tarea_id)
    contacto_tarea = ContactoTarea.objects.get(contacto=room)
    contacto_tarea.sector_tarea = sector_tarea
    contacto_tarea.save()

    return redirect('room:embudo', sector_tarea.sector.id)


'''
Versión 1:
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

---

Versión 2:
sector_tareas = SectorTarea.objects.filter(sector=sector)
contactos = Room.objects.filter(contacto_tarea__sector_tarea__sector=sector).distinct()

objeto_contactos = {}
for contacto in contactos:
    ultimo_mensaje = Message.objects.filter(contacto=contacto).order_by('-fecha_hora')[:1]
    sector_tarea = ContactoTarea.objects.get(contacto=contacto)
    objeto_contactos[contacto] = [sector_tarea, ultimo_mensaje]

objeto_sector_tareas = {}
for sector_tarea in sector_tareas:
    objeto_sector_tareas[sector_tarea] = []
    for room, lista in objeto_contactos.items():
        if lista[0].sector_tarea == sector_tarea:
            objeto_sector_tareas[sector_tarea].append([room, lista[1]])
'''