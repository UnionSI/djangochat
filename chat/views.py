from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.db.models import Max, Prefetch, Subquery, OuterRef, Q
from django.core import serializers
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import JsonResponse

from .models import Sector, SectorTarea, Contacto, Mensaje, ContactoTarea, ContactoIntegracion

from django.contrib.auth.models import User
from usuario.models import Usuario

from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import json, re

from config.settings import DEBUG

MENSAJES_POR_PAGINA = 15

@login_required
def chats(request):
    '''
    contactos = Contacto.objects.prefetch_related(
        Prefetch('messages', queryset=Mensaje.objects.order_by('-fecha_hora').first(), to_attr='last_mensaje')
    )
    '''
    lookups = Q()
    sectores_permitidos = request.user.sectores_permitidos()

    if sectores_permitidos:
        for sector_permitido in sectores_permitidos:
            lookups |= Q(contacto_integraciones__contacto_tareas__sector_tarea__sector=sector_permitido)
    else:
        return render(request, 'restringido.html')

    contactos_permitidos = Contacto.objects.filter(lookups) if sectores_permitidos else Contacto.objects.none()
    
    query = request.GET.get('buscar')
    if query:
        contactos = contactos_permitidos(Q(nombre__icontains=query) | Q(apellido__icontains=query) | Q(nro_socio=query) | Q(dni=query))
    else:
        contactos = contactos_permitidos

    contactos = contactos.annotate(
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
    sectores_permitidos = request.user.sectores_permitidos()
    
    contacto = get_object_or_404(Contacto.objects.prefetch_related('contacto_integraciones__integracion'), id=id)
    if not contacto.contacto_integraciones.first().contacto_tareas.first().sector_tarea.sector in sectores_permitidos:
        return render(request, 'restringido.html')

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
    nombres_usuarios = list(Usuario.objects.values_list('username', flat=True))
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
    #embudos = Sector.objects.all()
    sectores_permitidos = request.user.sectores_permitidos()

    if not sectores_permitidos:
        return render(request, 'restringido.html',)
    
    return render(request, 'chat/embudos.html', {'embudos': sectores_permitidos, 'debug': DEBUG})


@login_required
def embudo(request, id):
    sector = get_object_or_404(Sector, id=id)
    sectores_permitidos = request.user.sectores_permitidos()

    if not sector in sectores_permitidos:
        return render(request, 'restringido.html',)

    todos_los_sectores = Sector.objects.prefetch_related('sectortarea_set').all()
    #sector_tareas = SectorTarea.objects.filter(sector=sector).prefetch_related('contactotarea_set__contacto__mensajes').all()
    #sorted(sectores_tareas.contactotarea_set.contacto_integracion.contacto, key=lambda x: x.contacto_integraciones.first().mensajes.all().order_by('-fecha_hora').first().fecha_hora, reverse=True)

    # Obtener tareas
    sector_tareas = SectorTarea.objects.filter(sector=sector).prefetch_related('contactotarea_set__contacto_integracion__mensajes').all().order_by('orden')

    # Iterar sobre cada sector tarea y ordenar los contactos en función de la fecha_hora de su último mensaje
    #sector_tareas = SectorTarea.objects.filter(sector=sector).prefetch_related(
    #    Prefetch('contactotarea_set__contacto_integracion__mensajes', queryset=Mensaje.objects.order_by('-fecha_hora'))
    #).order_by('orden')

    sectores_tareas_preparadas = []

    for sector_tarea in sector_tareas:
        sector_tarea_info = {
            'id': sector_tarea.id,
            'nombre': sector_tarea.nombre,
            'contactos': []
        }
        for contacto_tarea in sector_tarea.contactotarea_set.all():
            contacto_integracion = contacto_tarea.contacto_integracion
            ultimo_mensaje = contacto_integracion.mensajes.last(),
            contacto_info = {
                'contacto_integracion_id': contacto_integracion.id,
                'nombre': contacto_integracion.contacto.nombre,
                'apellido': contacto_integracion.contacto.apellido,
                'nro_socio': contacto_integracion.contacto.nro_socio,
                'telefono': contacto_integracion.contacto.telefono,
                'dni': contacto_integracion.contacto.dni,
                'ultimo_mensaje_fecha_hora': ultimo_mensaje[0].fecha_hora if ultimo_mensaje else None,
                'ultimo_mensaje_usuario': ultimo_mensaje[0].usuario if ultimo_mensaje else None,
                'ultimo_mensaje_contenido': ultimo_mensaje[0].contenido if ultimo_mensaje else None,
            }
            sector_tarea_info['contactos'].append(contacto_info)
        sector_tarea_info['contactos'].sort(key=lambda x: x['ultimo_mensaje_fecha_hora'], reverse=True)
        sectores_tareas_preparadas.append(sector_tarea_info)


    '''
    # ¿Mejora la performance si se obtiene el último mensaje en la vista en lugar de pasarle todos los mensajes al template?
    # Agregar el último mensaje a cada Contacto
    for sector_tarea in sector_tareas:
        for contacto_tarea in sector_tarea.contactotarea_set.all():
            last_message = contacto_tarea.contacto.messages.order_by('-fecha_hora').first()
            contacto_tarea.last_message = last_message
    '''
    context = {'embudo': sector, 'embudos': sectores_permitidos, 'todos_los_sectores': todos_los_sectores, 'sector_tareas': sector_tareas, 'debug': DEBUG, 'sectores_tareas_preparadas': sectores_tareas_preparadas}
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
        'fecha': ultimo_mensaje.fecha_hora.strftime('%d-%m-%Y %H:%M'),
        #'type': 'sector_change',
        #'task_sector': sector_tarea.id,
        #'contacto': contacto,
        #'message': ultimo_mensaje.contenido,
        #'username': ultimo_mensaje.usuario if ultimo_mensaje.usuario else ultimo_mensaje.contacto.nombre,
    })
    return redirect('contacto:chat', contacto_id)


@login_required
def cargar_mas_mensajes(request, id, page):
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
        mencion = ''
        if mensaje.mensaje_citado:
            mencion = {
                'id': mensaje.mensaje_citado.id_integracion,
                'fecha_hora': mensaje.mensaje_citado.fecha_hora.strftime('%d/%m/%Y %H:%M'),
                'usuario': mensaje.mensaje_citado.usuario.username if mensaje.mensaje_citado.usuario else mensaje.mensaje_citado.contacto_integracion.contacto.nombre,
                'url_adjunto': mensaje.mensaje_citado.mensajes_adjuntos.first().archivo.url if mensaje.mensaje_citado.mensajes_adjuntos.first() else '',
                'mensaje': mensaje.mensaje_citado.contenido,
            }
        if mensaje.mensajes_adjuntos.first():
            print(mensaje.mensajes_adjuntos.first().archivo.url)
        mensajes_data.append({
            'mensaje': mensaje.contenido,
            'fecha_hora': mensaje.fecha_hora.strftime('%d/%m/%Y %H:%M'),
            'usuario': mensaje.usuario.username if mensaje.usuario else mensaje.contacto_integracion.contacto.nombre,
            'contacto_id': contacto.id,
            'url_adjunto': mensaje.mensajes_adjuntos.first().archivo.url if mensaje.mensajes_adjuntos.first() else '',
            'id_integracion': mensaje.id_integracion,
            'mencion': mencion
        })

    return JsonResponse({'status': 'success', 'mensajes': mensajes_data})
