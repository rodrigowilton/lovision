from django.contrib import admin
from django.urls import path, include
from django.conf import settings  # Importa as configurações do projeto
from django.conf.urls.static import static  # Necessário para servir arquivos estáticos e de mídia

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('descricao.urls')),
    path('', include('descricao.urls')),  # Inclui as URLs do app 'descricao'
]

# Servir arquivos de mídia no modo DEBUG
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
