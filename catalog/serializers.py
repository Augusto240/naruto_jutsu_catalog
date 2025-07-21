from rest_framework import serializers
from .models import Jutsu

class JutsuSerializer(serializers.ModelSerializer):
    element_display = serializers.CharField(source='get_element_type_display', read_only=True)
    type_display = serializers.CharField(source='get_jutsu_type_display', read_only=True)
    rank_display = serializers.CharField(source='get_rank_display', read_only=True)
    
    class Meta:
        model = Jutsu
        fields = [
            'id', 'name', 'description', 
            'element_type', 'element_display',
            'jutsu_type', 'type_display',
            'rank', 'rank_display',
            'image', 'created_at', 'updated_at'
        ]