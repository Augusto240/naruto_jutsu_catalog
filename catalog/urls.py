from django.urls import path
from .views import (
    HomeView,
    JutsuListView,
    JutsuDetailView,
    JutsuCreateView,
    JutsuUpdateView,
    JutsuDeleteView,
    DashboardView
)

urlpatterns = [
    # Página inicial
    path('', HomeView.as_view(), name='home'),
    
    # Lista de jutsus
    path('jutsus/', JutsuListView.as_view(), name='jutsu-list'),
    
    # Dashboard com estatísticas
    path('dashboard/', DashboardView.as_view(), name='dashboard'),

    # Detalhes do jutsu
    path('jutsu/<int:pk>/', JutsuDetailView.as_view(), name='jutsu-detail'),

    # Criar novo jutsu
    path('jutsu/criar/', JutsuCreateView.as_view(), name='jutsu-create'),

    # Editar jutsu
    path('jutsu/<int:pk>/editar/', JutsuUpdateView.as_view(), name='jutsu-edit'),

    # Excluir jutsu
    path('jutsu/<int:pk>/excluir/', JutsuDeleteView.as_view(), name='jutsu-delete'),
]