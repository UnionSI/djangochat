from django.contrib.auth import views as auth_views
from django.urls import path
from usuario.decorators import administrador_requirido

from . import views

urlpatterns = [
    path('', views.frontpage, name='frontpage'),
    path('signup/', views.signup, name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name='dashboard/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('drawflow/', views.drawflow,name='drawflow'),
    path('reportes/', views.MensajesListView.as_view(), name='reportes'),
    path('reportes/exportar-csv/', views.exportar_csv, name='exportar-csv'),
    path('administracion/', views.administracion, name='administracion'),
    path('administracion/sector/lista/', administrador_requirido(views.SectorListView.as_view()), name='sector-lista'),
    path('administracion/sector/crear/', administrador_requirido(views.SectorCreateView.as_view()), name='sector-crear'),
    path('administracion/sector/detalle/<int:pk>', administrador_requirido(views.SectorDetailView.as_view()), name='sector-detalle'),
    path('administracion/sector/actualizar/<int:pk>', administrador_requirido(views.SectorUpdateView.as_view()), name='sector-actualizar'),
    path('administracion/sector/borrar/<int:pk>', administrador_requirido(views.SectorDeleteView.as_view()), name='sector-borrar'),
    path('administracion/tarea/lista/', administrador_requirido(views.SectorTareaListView.as_view()), name='tarea-lista'),
    path('administracion/tarea/crear/', administrador_requirido(views.SectorTareaCreateView.as_view()), name='tarea-crear'),
    path('administracion/tarea/detalle/<int:pk>', administrador_requirido(views.SectorTareaDetailView.as_view()), name='tarea-detalle'),
    path('administracion/tarea/actualizar/<int:pk>', administrador_requirido(views.SectorTareaUpdateView.as_view()), name='tarea-actualizar'),
    path('administracion/tarea/borrar/<int:pk>', administrador_requirido(views.SectorTareaDeleteView.as_view()), name='tarea-borrar'),
    path('administracion/usuario/lista/', administrador_requirido(views.UsuarioListView.as_view()), name='usuario-lista'),
    path('administracion/usuario/crear/', administrador_requirido(views.UsuarioCreateView.as_view()), name='usuario-crear'),
    path('administracion/usuario/detalle/<int:pk>', administrador_requirido(views.UsuarioDetailView.as_view()), name='usuario-detalle'),
    path('administracion/usuario/actualizar/<int:pk>', administrador_requirido(views.UsuarioUpdateView.as_view()), name='usuario-actualizar'),
    path('administracion/usuario/borrar/<int:pk>', administrador_requirido(views.UsuarioDeleteView.as_view()), name='usuario-borrar'),
    path('administracion/usuario/cambiar-clave/<int:pk>/', administrador_requirido(views.AdminCambiarClaveView.as_view()), name='cambiar-clave'),
]