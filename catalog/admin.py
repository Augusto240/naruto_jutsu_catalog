# catalog/admin.py
from django.contrib import admin
from .models import Jutsu

@admin.register(Jutsu)
class JutsuAdmin(admin.ModelAdmin):
    list_display = [
        'name',                    
        'element_type',           
        'get_element_display',    
        'jutsu_type',
        'rank', 
        'created_at'
    ]
    list_filter = [
        'element_type',          
        'jutsu_type',             
        'rank',                 
        'created_at',            
    ]

    search_fields = [
        'name',                  
        'description',           
    ]

    ordering = ['name']
    
    readonly_fields = ['created_at', 'updated_at']

    fieldsets = (
        ('Informações Básicas', {
            'fields': ('name', 'description')
        }),
        ('Classificação', {
            'fields': ('element_type', 'jutsu_type', 'rank'),
            'classes': ('wide',),  
        }),
        ('Metadados', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',), 
        }),
    )
    list_per_page = 25
    
    def get_element_display(self, obj):
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
    
    get_element_display.short_description = 'Elemento'