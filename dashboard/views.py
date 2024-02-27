from django.contrib.auth import login
from django.urls import reverse, reverse_lazy
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.views import PasswordChangeView
from .forms import SectorForm, SectorTareaForm, CrearUsuarioForm, ActualizarUsuarioForm, AdminCambiarClaveForm
from django.contrib.auth.models import User
from usuario.models import Usuario, Perfil
from usuario.decorators import administrador_requirido
from django.contrib.auth.forms import AuthenticationForm
from chat.models import Sector, SectorTarea, Mensaje
from django.db.models import Q
import csv, datetime
from django.http import HttpResponse
from datetime import datetime


@login_required
def frontpage(request):
    return render(request, 'dashboard/frontpage.html')


def signup(request):
    if request.method == 'POST':
        form = AuthenticationForm(request.POST)

        if form.is_valid():
            user = form.save()

            login(request, user)

            return redirect('frontpage')
    else:
        form = AuthenticationForm()
    
    return render(request, 'dashboard/signup.html', {'form': form})


@administrador_requirido
def drawflow(request):
    nodos = ['Facebook', 'Github', 'Twitter']
    return render(request, 'dashboard/drawflow.html', {'nodos': nodos})



@administrador_requirido
def administracion(request):
    return render(request, 'dashboard/admin/admin.html')

""" ---------------"""
""" Vista Reportes """

def get_queryset_mensajes(request, queryset=Mensaje.objects.all()):
    sectores_id = request.GET.getlist('sector')
    tareas_id = request.GET.getlist('tarea')
    usuarios_id = request.GET.getlist('usuario')
    desde = request.GET.get('desde')
    hasta = request.GET.get('hasta')
    ordenar = request.GET.get('ordenar')

    if desde:
        desde_dt = datetime.strptime(desde, '%Y-%m-%d').replace(hour=0, minute=0, second=0)
        queryset = queryset.filter(fecha_hora__gte=desde_dt)

    if hasta:
        hasta_dt = datetime.strptime(hasta, '%Y-%m-%d').replace(hour=23, minute=59, second=59)
        queryset = queryset.filter(fecha_hora__lte=hasta_dt)

    if sectores_id:
        lookups = Q()
        for sector_id in sectores_id:
            lookup = Q(contacto_integracion__contacto_tareas__sector_tarea__sector__id=sector_id)
            lookups |= lookup
        queryset = queryset.filter(lookups)

    if tareas_id:
        lookups = Q()
        for tarea_id in tareas_id:
            lookup = Q(contacto_integracion__contacto_tareas__sector_tarea__id=tarea_id)
            lookups |= lookup
        queryset = queryset.filter(lookups)

    if usuarios_id:
        lookups = Q()
        for usuario_id in usuarios_id:
            lookup = Q(usuario__id=usuario_id)
            lookups |= lookup
        queryset = queryset.filter(lookups)

    if ordenar:
        mapeo = {
            'sector': 'contacto_integracion__contacto_tareas__sector_tarea__sector__nombre',
            '-sector': '-contacto_integracion__contacto_tareas__sector_tarea__sector__nombre',
            'tarea': 'contacto_integracion__contacto_tareas__sector_tarea__nombre',
            '-tarea': '-contacto_integracion__contacto_tareas__sector_tarea__nombre',
            'contacto': 'contacto_integracion__contacto__nombre',
            '-contacto': '-contacto_integracion__contacto__nombre',
            'integracion': 'contacto_integracion__integracion__nombre',
            '-integracion': '-contacto_integracion__integracion__nombre',
            'dni': 'contacto_integracion__contacto__dni',
            '-dni': '-contacto_integracion__contacto__dni',
            'telefono': 'contacto_integracion__contacto__telefono',
            '-telefono': '-contacto_integracion__contacto__telefono',
            'empresa': 'contacto_integracion__contacto__empresa',
            '-empresa': '-contacto_integracion__contacto__empresa',
            'nro_socio': 'contacto_integracion__contacto__nro_socio',
            '-nro_socio': '-contacto_integracion__contacto__nro_socio',
        }

        ordenar_mapeado = mapeo.get(ordenar, ordenar)
        queryset = queryset.order_by(ordenar_mapeado)
    
    return queryset


class MensajesListView(ListView):
    model = Mensaje
    paginate_by = 20
    template_name = 'dashboard/reportes.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        return get_queryset_mensajes(self.request, queryset)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        sectores_id = self.request.GET.getlist('sector')
        tareas_id = self.request.GET.getlist('tarea')
        usuarios_id = self.request.GET.getlist('usuario')
        desde = self.request.GET.get('desde')
        hasta = self.request.GET.get('hasta')
        ordenar = self.request.GET.get('ordenar')

        if sectores_id:
            context['filtro_sectores'] = sectores_id
        if tareas_id:
            context['filtro_tareas'] = tareas_id
        if usuarios_id:
            context['filtro_usuarios'] = usuarios_id
        if desde:
            context['filtro_desde'] = desde
        if hasta:
            context['filtro_hasta'] = hasta
        if ordenar:
            context['filtro_ordenar'] = ordenar

        query_params = self.request.GET.dict()
        if 'ordenar' in query_params:
            del query_params['ordenar']

        context.update({
            'sectores': Sector.objects.all(),
            'tareas': SectorTarea.objects.all(),
            'usuarios': Usuario.objects.all(),
            'query_params': '&'.join([f'{key}={value}' for key, value in query_params.items()])
        })
        return context


@administrador_requirido
def exportar_csv(request):
    response = HttpResponse(content_type='text/csv', charset='utf-8')
    now = str(datetime.now())
    response['Content-Disposition'] = f'attachment; filename="{now}.csv"'
    response.write(u'\ufeff'.encode('utf8'))

    #queryset = Mensaje.objects.all()   
    queryset = get_queryset_mensajes(request)

    writer = csv.writer(response, delimiter=';')

    # Encabezados de columna
    writer.writerow([
        'sector',
        'tarea',
        'nombre_contacto',
        'contenido',
        'enviado_por',
        'mensaje_citado',
        'recibido',
        'leido',
        'fecha_hora',
        'integracion',
        'dni', 
        'telefono', 
        'email', 
        'empresa', 
        'nro_socio'
    ])

    # Campos de datos
    for objeto in queryset:
        contacto = objeto.contacto_integracion.contacto
        nombre_contacto = f'{contacto.nombre} {contacto.apellido}'
        sector_tarea = objeto.contacto_integracion.contacto_tareas.first().sector_tarea
        writer.writerow([
            sector_tarea.sector,
            sector_tarea.nombre,
            nombre_contacto,
            objeto.contenido,
            objeto.usuario if objeto.usuario else nombre_contacto,
            ' ',#objeto.mensaje_citado.contenido if objeto.mensaje_citado.contenido else '',
            objeto.recibido,
            objeto.leido,
            objeto.fecha_hora,
            objeto.contacto_integracion.integracion.nombre,
            contacto.dni,
            contacto.telefono,
            contacto.email,
            contacto.empresa,
            contacto.nro_socio,
        ])

    return response

""" --------------------- """
""" Vista de ABM Sectores """

class SectorListView(ListView):
    model = Sector
    paginate_by = 10
    template_name = 'dashboard/admin/sector/list.html'

class SectorDetailView(DetailView):
    model = Sector
    template_name = 'dashboard/admin/sector/detail.html'

class SectorCreateView(CreateView):
    model = Sector
    form_class = SectorForm
    template_name = 'dashboard/admin/sector/form.html'
    success_url = reverse_lazy('sector-lista')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'titulo_vista': 'Crear Sector',
            'descripcion_vista': 'Nuevo registro'
        })
        return context

class SectorUpdateView(UpdateView):
    model = Sector
    form_class = SectorForm
    template_name = 'dashboard/admin/sector/form.html'
    success_url = reverse_lazy('sector-lista')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'titulo_vista': 'Actualizar Sector',
            'descripcion_vista': 'Actualizar datos'
        })
        return context

class SectorDeleteView(DeleteView):
    model = Sector
    template_name = 'dashboard/admin/sector/delete.html'
    success_url = reverse_lazy('sector-lista')


""" ----------------- """
""" Vistas ABM Tareas """

class SectorTareaListView(ListView):
    model = SectorTarea
    paginate_by = 20
    template_name = 'dashboard/admin/tarea/list.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        sector_id = self.request.GET.get('sector')
        ordenar = self.request.GET.get('ordenar')
        if sector_id:
            lookup = Q(sector__id=sector_id)
            queryset = queryset.filter(lookup)
        if ordenar:
            queryset = queryset.order_by(ordenar)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.GET.get('sector'):
            context['sector'] = self.request.GET.get('sector')
        if self.request.GET.get('ordenar'):
            context['ordenar'] = self.request.GET.get('ordenar')
        context.update({
            'titulo_vista': 'Crear Tarea',
            'descripcion_vista': 'Nuevo registro',
            'sectores': Sector.objects.all()
        })
        return context

class SectorTareaDetailView(DetailView):
    model = SectorTarea
    template_name = 'dashboard/admin/tarea/detail.html'

class SectorTareaCreateView(CreateView):
    model = SectorTarea
    form_class = SectorTareaForm
    template_name = 'dashboard/admin/tarea/form.html'
    success_url = reverse_lazy('tarea-lista')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'titulo_vista': 'Crear Tarea',
            'descripcion_vista': 'Nuevo registro',
        })
        return context

class SectorTareaUpdateView(UpdateView):
    model = SectorTarea
    form_class = SectorTareaForm
    template_name = 'dashboard/admin/tarea/form.html'
    success_url = reverse_lazy('tarea-lista')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'titulo_vista': 'Actualizar Tarea',
            'descripcion_vista': 'Actualizar datos'
        })
        return context

class SectorTareaDeleteView(DeleteView):
    model = SectorTarea
    template_name = 'dashboard/admin/tarea/delete.html'
    success_url = reverse_lazy('tarea-lista')
    

""" ----------------- """
""" Vistas ABM Usuarios """

class UsuarioListView(ListView):
    model = Usuario
    paginate_by = 10
    template_name = 'dashboard/admin/usuario/list.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        perfil_id = self.request.GET.get('perfil')
        ordenar = self.request.GET.get('ordenar')
        if perfil_id:
            lookup = Q(perfil__id=perfil_id)
            queryset = queryset.filter(lookup)
        if ordenar:
            queryset = queryset.order_by(ordenar)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.GET.get('perfil'):
            context['perfil'] = self.request.GET.get('perfil')
        if self.request.GET.get('ordenar'):
            context['ordenar'] = self.request.GET.get('ordenar')
        context.update({
            'titulo_vista': 'Crear Tarea',
            'descripcion_vista': 'Nuevo registro',
            'perfiles': Perfil.objects.all()
        })
        return context

class UsuarioDetailView(DetailView):
    model = Usuario
    template_name = 'dashboard/admin/usuario/detail.html'

class UsuarioCreateView(CreateView):
    model = Usuario
    form_class = CrearUsuarioForm
    template_name = 'dashboard/admin/usuario/form.html'
    success_url = reverse_lazy('usuario-lista')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'titulo_vista': 'Crear Usuario',
            'descripcion_vista': 'Nuevo registro'
        })
        return context

class UsuarioUpdateView(UpdateView):
    model = Usuario
    form_class = ActualizarUsuarioForm
    template_name = 'dashboard/admin/usuario/form.html'
    success_url = reverse_lazy('usuario-lista')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'titulo_vista': 'Actualizar',
            'descripcion_vista': 'Cambiar datos del usuario'
        })
        return context

class UsuarioDeleteView(DeleteView):
    model = Usuario
    template_name = 'dashboard/admin/usuario/delete.html'
    success_url = reverse_lazy('usuario-lista')

class AdminCambiarClaveView(PasswordChangeView):
    model = Usuario
    form_class = AdminCambiarClaveForm
    template_name = 'dashboard/admin/usuario/cambiar_clave.html'
    success_url = reverse_lazy('usuario-lista')

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_id = self.kwargs.get('pk')
        print(user_id)
        user = Usuario.objects.get(pk=user_id)
        print(user)
        context['username'] = user.username
        return context

    
