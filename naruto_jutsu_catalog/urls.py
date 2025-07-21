from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import routers, permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from catalog.api_views import JutsuViewSet

# Configuração do Swagger para documentação da API
schema_view = get_schema_view(
   openapi.Info(
      title="Naruto Jutsu Catalog API",
      default_version='v1',
      description="API para o catálogo de jutsus de Naruto",
      terms_of_service="https://www.example.com/terms/",
      contact=openapi.Contact(email="seu.email@example.com"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=[permissions.AllowAny],
)

# Configuração do roteador da API
router = routers.DefaultRouter()
router.register(r'jutsus', JutsuViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),    
    path('', include('catalog.urls')),  # URLs da aplicação web
    path('api/', include(router.urls)),  # URLs da API REST
    path('api-auth/', include('rest_framework.urls')),  # URLs de autenticação da API
    
    # Django Debug Toolbar
    path('__debug__/', include('debug_toolbar.urls')),
    
    # Swagger/ReDoc
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]

# Servir arquivos de mídia durante o desenvolvimento
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)