from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.db.models import Prefetch
from django.db.models import Max, Subquery, OuterRef
from django.core import serializers
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .models import Sector, SectorTarea, Contacto, Mensaje, ContactoTarea, ContactoIntegracion
from django.contrib.auth.models import User

from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import json, re

from config.settings import DEBUG

MENSAJES_POR_PAGINA = 10

@login_required
def chats(request):
    '''
    contactos = Contacto.objects.prefetch_related(
        Prefetch('messages', queryset=Mensaje.objects.order_by('-fecha_hora').first(), to_attr='last_mensaje')
    )
    '''
    contactos = Contacto.objects.annotate(
        last_message_content=Subquery(
            Mensaje.objects.filter(contacto_integracion=OuterRef('pk')).values('contenido').order_by('-fecha_hora')[:1]
        ),
        last_message_date=Subquery(
            Mensaje.objects.filter(contacto_integracion=OuterRef('pk')).values('fecha_hora').order_by('-fecha_hora')[:1]
        ),
        last_message_user=Subquery(
            Mensaje.objects.filter(contacto_integracion=OuterRef('pk')).values('usuario__username').order_by('-fecha_hora')[:1]
        )
    )
    context = {'contactos': contactos, 'debug': DEBUG}
    if request.path == '/contacto/chat-dev/todos': # Para Tests
        return render(request, 'chat/chatsdev.html', context)
    else:
        return render(request, 'chat/chats.html', context)


@login_required
def chat(request, id):
    contacto = get_object_or_404(Contacto.objects.prefetch_related('contacto_integraciones__integracion'), id=id)
    contacto_integracion = contacto.contacto_integraciones.first()
    integracion = contacto_integracion.integracion.nombre
    contacto_tarea = contacto_integracion.contacto_tareas.first()
    sector_tarea = contacto_tarea.sector_tarea
    sectores = Sector.objects.prefetch_related('sectortarea_set').all()    
    contacto_mensajes = Mensaje.objects.filter(contacto_integracion__contacto=contacto).order_by('-fecha_hora')[:MENSAJES_POR_PAGINA]  # Ver cómo manejar esto si hay muchos mensajes
    contacto_mensajes = sorted(contacto_mensajes, key=lambda x: x.fecha_hora)

    contactos = Contacto.objects.annotate(
        last_message_content=Subquery(
            Mensaje.objects.filter(contacto_integracion=OuterRef('pk')).values('contenido').order_by('-fecha_hora')[:1]
        ),
        last_message_date=Subquery(
            Mensaje.objects.filter(contacto_integracion=OuterRef('pk')).values('fecha_hora').order_by('-fecha_hora')[:1]
        ),
        last_message_user=Subquery(
            Mensaje.objects.filter(contacto_integracion=OuterRef('pk')).values('usuario__username').order_by('-fecha_hora')[:1]
        )
    )
    nombres_usuarios = list(User.objects.values_list('username', flat=True))
    context = {
        'contacto': contacto,
        'contacto_mensajes': contacto_mensajes,
        'contactos': contactos,
        'integracion': integracion,
        'sector_tarea': sector_tarea,
        'embudos': sectores, 
        'usuario_asignado': contacto_tarea.usuario,
        'usuarios': nombres_usuarios,
        'debug': DEBUG
    }
    if re.search('/contacto/chat-dev/', request.path):  # Para Tests
        return render(request, 'chat/chatsdev.html', context)
    else:
        return render(request, 'chat/detalle_chat.html', context)


@login_required
def embudos(request):
    embudos = Sector.objects.all()
    return render(request, 'chat/embudos.html', {'embudos': embudos, 'debug': DEBUG})


@login_required
def embudo(request, id):
    sector = get_object_or_404(Sector, id=id)
    sectores = Sector.objects.prefetch_related('sectortarea_set').all()    
    #sector_tareas = SectorTarea.objects.filter(sector=sector).prefetch_related('contactotarea_set__contacto__mensajes').all()
    sector_tareas = SectorTarea.objects.filter(sector=sector).prefetch_related('contactotarea_set__contacto_integracion__mensajes').all()
    '''
    # ¿Mejora la performance si se obtiene el último mensaje en la vista en lugar de pasarle todos los mensajes al template?
    # Agregar el último mensaje a cada Contacto
    for sector_tarea in sector_tareas:
        for contacto_tarea in sector_tarea.contactotarea_set.all():
            last_message = contacto_tarea.contacto.messages.order_by('-fecha_hora').first()
            contacto_tarea.last_message = last_message
    '''
    context = {'embudo': sector, 'embudos': sectores, 'sector_tareas': sector_tareas, 'debug': DEBUG}
    return render(request, 'chat/embudos.html', context)
    

@login_required
@require_POST
def mover_de_sector(request, contacto_id, sector_tarea_id):
    contacto = get_object_or_404(Contacto, id=contacto_id)
    contacto_integracion = ContactoIntegracion.objects.get(contacto=contacto)
    contacto_tarea = ContactoTarea.objects.get(contacto_integracion=contacto_integracion)
    ultimo_mensaje = Mensaje.objects.filter(contacto_integracion=contacto_integracion).order_by('-fecha_hora').first()
    #ultimo_mensaje = Mensaje.objects.filter(contacto_integracion=contacto_integracion).prefetch_related('contacto', 'usuario').order_by('-fecha_hora').first()
    sector_tarea = get_object_or_404(SectorTarea, id=sector_tarea_id)
    contacto_tarea.sector_tarea = sector_tarea
    contacto_tarea.save()
    # Enviar mensaje a través de WebSocket
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)('global', {
        'type': 'sector_change',
        'sector': sector_tarea.sector.nombre,
        'sector_tarea': sector_tarea.nombre,
        'contacto': contacto.nombre,
        'slug': contacto.id,
        'no_leido': '',
        'thumbnail': '',
        'cabecera': contacto.nombre,
        'dni': contacto.dni,
        'usuario': ultimo_mensaje.usuario.username if ultimo_mensaje.usuario else contacto.nombre,
        'mensaje': ultimo_mensaje.contenido,
        'fecha': ultimo_mensaje.fecha_hora.strftime('%Y-%m-%d %H:%M:%S'),
        #'type': 'sector_change',
        #'task_sector': sector_tarea.id,
        #'contacto': contacto,
        #'message': ultimo_mensaje.contenido,
        #'username': ultimo_mensaje.usuario if ultimo_mensaje.usuario else ultimo_mensaje.contacto.nombre,
    })
    return redirect('contacto:chat', contacto_id)


from django.http import JsonResponse

def load_more_messages(request, id, page):
    contacto = get_object_or_404(Contacto.objects.prefetch_related('contacto_integraciones__integracion'), id=id)
    contacto_mensajes = Mensaje.objects.filter(contacto_integracion__contacto=contacto)
    
    # Paginación
    paginator = Paginator(contacto_mensajes.order_by('-fecha_hora'), MENSAJES_POR_PAGINA)
    try:
        mensajes_pagina = paginator.page(page)
    except Exception as error:
        return JsonResponse({'status': str(error)})

    # Preparar datos de mensajes para la respuesta JSON
    mensajes_data = []
    for mensaje in mensajes_pagina:
        mensajes_data.append({
            'mensaje': mensaje.contenido,
            'fecha_hora': mensaje.fecha_hora.strftime('%d/%m/%Y %H:%M'),
            'usuario': mensaje.usuario.username if mensaje.usuario else mensaje.contacto_integracion.contacto.nombre,
            'url_adjunto': mensaje.mensajes_adjuntos.first().archivo.url if mensaje.mensajes_adjuntos.first() else ''
        })

    return JsonResponse({'status': 'success', 'mensajes': mensajes_data})
