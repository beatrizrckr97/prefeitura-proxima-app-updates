from django.contrib import admin

from .models import Chamado
from .models import UsuarioSistema

# Register your models here.
admin.site.register(Chamado)
@admin.register(UsuarioSistema)
class UsuarioSistema(admin.ModelAdmin):
    list_display = ('nome', 'email', 'cpf', 'role')
    search_fields = ('nome', 'email', 'cpf')
    list_filter = ('role',)