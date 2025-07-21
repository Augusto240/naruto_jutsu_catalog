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
    path('', HomeView.as_view(), name='home'),
        
    path('jutsus/', JutsuListView.as_view(), name='jutsu-list'),
        
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    
    path('jutsu/<int:pk>/', JutsuDetailView.as_view(), name='jutsu-detail'),

    path('jutsu/criar/', JutsuCreateView.as_view(), name='jutsu-create'),

    path('jutsu/<int:pk>/editar/', JutsuUpdateView.as_view(), name='jutsu-edit'),

    path('jutsu/<int:pk>/excluir/', JutsuDeleteView.as_view(), name='jutsu-delete'),
]