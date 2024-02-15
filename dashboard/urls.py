from django.contrib.auth import views as auth_views
from django.urls import path

from . import views

urlpatterns = [
    path('', views.frontpage, name='frontpage'),
    path('signup/', views.signup, name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name='dashboard/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('drawflow/', views.drawflow, name='drawflow'),
    path('administracion/', views.administracion, name='administracion'),
    path('administracion/sector/lista', views.SectorListView.as_view(), name='sector-lista'),
    path('administracion/sector/crear/', views.SectorCreateView.as_view(), name='sector-crear'),
    path('administracion/sector/detalle/<int:pk>', views.SectorDetailView.as_view(), name='sector-detalle'),
    path('administracion/sector/actualizar/<int:pk>', views.SectorUpdateView.as_view(), name='sector-actualizar'),
    path('administracion/sector/borrar/<int:pk>', views.SectorDeleteView.as_view(), name='sector-borrar'),
    path('administracion/tarea/lista', views.SectorTareaListView.as_view(), name='tarea-lista'),
    path('administracion/tarea/crear/', views.SectorTareaCreateView.as_view(), name='tarea-crear'),
    path('administracion/tarea/detalle/<int:pk>', views.SectorTareaDetailView.as_view(), name='tarea-detalle'),
    path('administracion/tarea/actualizar/<int:pk>', views.SectorTareaUpdateView.as_view(), name='tarea-actualizar'),
    path('administracion/tarea/borrar/<int:pk>', views.SectorTareaDeleteView.as_view(), name='tarea-borrar'),
    path('administracion/usuario/lista', views.UsuarioListView.as_view(), name='usuario-lista'),
    path('administracion/usuario/crear/', views.UsuarioCreateView.as_view(), name='usuario-crear'),
    path('administracion/usuario/detalle/<int:pk>', views.UsuarioDetailView.as_view(), name='usuario-detalle'),
    path('administracion/usuario/actualizar/<int:pk>', views.UsuarioUpdateView.as_view(), name='usuario-actualizar'),
    path('administracion/usuario/borrar/<int:pk>', views.UsuarioDeleteView.as_view(), name='usuario-borrar'),
    path('administracion/usuario/cambiar-contraseña/<int:pk>/', views.AdminCambiarContraseñaView.as_view(), name='cambiar-contraseña'),

]