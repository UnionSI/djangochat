from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from usuario.models import Usuario
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AdminPasswordChangeForm
from chat.models import Sector, SectorTarea
from django.utils.translation import gettext, gettext_lazy as _


class SectorForm(forms.ModelForm):
    class Meta:
        model = Sector
        fields = ('__all__')

    def __init__(self, *args, **kwargs):
        super(SectorForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = "form-control"


class SectorTareaForm(forms.ModelForm):
    class Meta:
        model = SectorTarea
        fields = ('nombre', 'sector', 'orden', 'activo')

    def __init__(self, *args, **kwargs):
        super(SectorTareaForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = "form-control"
            self.fields['activo'].widget = forms.CheckboxInput(attrs={'class': 'form-check-input'})


class CrearUsuarioForm(UserCreationForm):
    class Meta:
        model = Usuario
        fields = ('username', 'password1', 'password2', 'perfil', 'first_name', 'last_name', 'email', 'groups', 'is_active')
        #fields = ('__all__')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            self.fields['is_active'].widget = forms.CheckboxInput(attrs={'class': 'form-check-input'})


class ActualizarUsuarioForm(UserChangeForm):
    password = None

    class Meta:
        model = Usuario
        fields = ('username', 'perfil', 'first_name', 'last_name', 'email', 'groups', 'is_active')
        #fields = ('__all__')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            self.fields['is_active'].widget = forms.CheckboxInput(attrs={'class': 'form-check-input'})


class AdminCambiarClaveForm(AdminPasswordChangeForm):
    class Meta:
        model = Usuario
        #fields = ('__all__')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
