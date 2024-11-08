from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from .views import home

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('custom_auth.urls')),
    path('documents/', include('documents.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

