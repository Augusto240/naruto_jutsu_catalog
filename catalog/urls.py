from django.urls import path
from .views import (
    JutsuListView,
    JutsuDetailView,
    JutsuCreateView,
    JutsuUpdateView,
    JutsuDeleteView,
    DashboardView
)

urlpatterns = [
    # Caminho Raiz: '' (vazio) -> A "página inicial" do nosso app.
    path('', JutsuListView.as_view(), name='jutsu-list'),

    # Dashboard com estatísticas
    path('dashboard/', DashboardView.as_view(), name='dashboard'),

    # Caminho para Detalhes: 'jutsu/<int:pk>/'
    path('jutsu/<int:pk>/', JutsuDetailView.as_view(), name='jutsu-detail'),

    # Caminho para Criar: 'jutsu/criar/'
    path('jutsu/criar/', JutsuCreateView.as_view(), name='jutsu-create'),

    # Caminho para Editar: 'jutsu/<int:pk>/editar/'
    path('jutsu/<int:pk>/editar/', JutsuUpdateView.as_view(), name='jutsu-edit'),

    # Caminho para Excluir: 'jutsu/<int:pk>/excluir/'
    path('jutsu/<int:pk>/excluir/', JutsuDeleteView.as_view(), name='jutsu-delete'),
]