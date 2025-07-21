from rest_framework import viewsets, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Jutsu
from .serializers import JutsuSerializer

class JutsuViewSet(viewsets.ModelViewSet):
    """
    API endpoint para visualizar e editar jutsus.
    
    Um ViewSet no DRF fornece automaticamente operações CRUD:
    - list (GET): listar todos os jutsus
    - retrieve (GET): obter um jutsu específico
    - create (POST): criar um novo jutsu
    - update (PUT/PATCH): atualizar um jutsu
    - destroy (DELETE): excluir um jutsu
    """
    queryset = Jutsu.objects.all().order_by('name')
    serializer_class = JutsuSerializer
    
    # Sistemas de filtragem
    filter_backends = [
        DjangoFilterBackend,  # Permite filtros por campo
        filters.SearchFilter,  # Permite busca em campos específicos
        filters.OrderingFilter  # Permite ordenação
    ]
    
    # Configurações para cada sistema de filtragem
    filterset_fields = ['element_type', 'jutsu_type', 'rank']  # ?element_type=fire
    search_fields = ['name', 'description']  # ?search=rasengan
    ordering_fields = ['name', 'created_at', 'rank']  # ?ordering=name ou ?ordering=-created_at
    
    # Permissões - apenas usuários autenticados podem editar
    def get_permissions(self):
        """
        Define permissões diferentes dependendo da ação.
        - Listar/ver jutsus: qualquer um pode
        - Criar/editar/deletar: apenas usuários autenticados
        """
        if self.action in ['list', 'retrieve']:
            permission_classes = [permissions.AllowAny]
        else:
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]