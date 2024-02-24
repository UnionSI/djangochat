from django.contrib.auth import login
from django.urls import reverse, reverse_lazy
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.views import PasswordChangeView
from .forms import SectorForm, SectorTareaForm, CrearUsuarioForm, ActualizarUsuarioForm, AdminCambiarClaveForm
from django.contrib.auth.models import User
from usuario.models import Usuario
from django.contrib.auth.forms import AuthenticationForm
from chat.models import Sector, SectorTarea
from django.db.models import Q


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


def drawflow(request):
    nodos = ['Facebook', 'Github', 'Twitter']
    return render(request, 'dashboard/drawflow.html', {'nodos': nodos})


def administracion(request):
    return render(request, 'dashboard/admin/admin.html')


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
        #perfil_id = self.request.GET.get('perfil')
        ordenar = self.request.GET.get('ordenar')
        """ if perfil_id:
            lookup = Q(perfil__id=perfil_id)
            queryset = queryset.filter(lookup) """
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
            #'perfiles': Sector.objects.all()
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

    
