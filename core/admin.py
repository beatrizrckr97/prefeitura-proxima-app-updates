from django.contrib import admin

from .models import Chamado
from .models import UsuarioSistema

# Register your models here.
admin.site.register(Chamado)
@admin.register(UsuarioSistema)
class UsuarioSistemaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'email', 'cpf', 'role', 'is_approved')
    list_editable = ('is_approved',)  # permite editar direto na lista
    search_fields = ('nome', 'email', 'cpf')
    list_filter = ('role', 'is_approved')