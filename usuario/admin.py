from django.contrib import admin
from .models import Usuario, Perfil, PerfilSector

# Register your models here.

@admin.register(Usuario)
class AdminUsuario(admin.ModelAdmin):
    list_display = ('username', 'perfil', 'email', 'first_name', 'last_name', 'is_staff', 'is_active')
    search_fields = ('username', 'first_name', 'last_name', 'email')

@admin.register(Perfil)
class AdminPerfil(admin.ModelAdmin):
    list_display = ('nombre',)
    
@admin.register(PerfilSector)
class AdminPerfilSector(admin.ModelAdmin):
    list_display = ('perfil', 'sector')