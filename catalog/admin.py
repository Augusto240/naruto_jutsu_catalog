# catalog/admin.py
from django.contrib import admin
from .models import Jutsu

# VERSÃO BÁSICA (funciona, mas é simples)
# admin.site.register(Jutsu)

# VERSÃO AVANÇADA (muito mais poderosa)
@admin.register(Jutsu)
class JutsuAdmin(admin.ModelAdmin):
    """
    Configuração personalizada para o modelo Jutsu no admin.
    
    Pense nisso como criar uma interface especializada para
    os arquivistas ninja gerenciarem o catálogo de jutsus.
    """
    
    # Campos mostrados na lista principal
    list_display = [
        'name',                    # Nome do jutsu
        'element_type',           # Elemento (mas vai mostrar o código)
        'get_element_display',    # Elemento (versão legível)
        'jutsu_type',
        'rank', 
        'created_at'
    ]
    
    # Filtros na barra lateral - super úteis para navegar
    list_filter = [
        'element_type',           # Filtro por elemento
        'jutsu_type',            # Filtro por tipo  
        'rank',                  # Filtro por rank
        'created_at',            # Filtro por data de criação
    ]
    
    # Campos pesquisáveis - cria uma caixa de busca
    search_fields = [
        'name',                  # Buscar por nome
        'description',           # Buscar na descrição
    ]
    
    # Ordenação padrão
    ordering = ['name']
    
    # Campos somente leitura - usuários podem ver mas não editar
    readonly_fields = ['created_at', 'updated_at']
    
    # Organização dos campos no formulário de edição
    fieldsets = (
        ('Informações Básicas', {
            'fields': ('name', 'description')
        }),
        ('Classificação', {
            'fields': ('element_type', 'jutsu_type', 'rank'),
            'classes': ('wide',),  # Layout mais largo
        }),
        ('Metadados', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),  # Seção colapsável
        }),
    )
    
    # Quantos itens mostrar por página
    list_per_page = 25
    
    # Método personalizado para mostrar elemento de forma mais bonita
    def get_element_display(self, obj):
        """Retorna o elemento com emoji visual."""
        element_emojis = {
            'fire': '🔥',
            'water': '🌊', 
            'wind': '💨',
            'earth': '🗿',
            'lightning': '⚡',
            'illusion': '👁️',
            'yin': '☯️',
            'yang': '☯️', 
            'yin-yang': '☯️',
            'other': '❓'
        }
        emoji = element_emojis.get(obj.element_type, '❓')
        return f"{emoji} {obj.get_element_type_display()}"
    
    # Nome da coluna no admin
    get_element_display.short_description = 'Elemento'