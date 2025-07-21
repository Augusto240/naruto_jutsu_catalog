from rest_framework import viewsets, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Jutsu
from .serializers import JutsuSerializer

class JutsuViewSet(viewsets.ModelViewSet):
    queryset = Jutsu.objects.all().order_by('name')
    serializer_class = JutsuSerializer
    filter_backends = [
        DjangoFilterBackend,  
        filters.SearchFilter, 
        filters.OrderingFilter 
    ]

    filterset_fields = ['element_type', 'jutsu_type', 'rank'] 
    search_fields = ['name', 'description']  
    ordering_fields = ['name', 'created_at', 'rank']  

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            permission_classes = [permissions.AllowAny]
        else:
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]