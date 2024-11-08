from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views

app_name = 'auth'

urlpatterns = [
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('registro/', views.registro, name='registro'),
    path('seguridad/', views.seguridad, name='seguridad'),
    path('seguridad/configurar-2fa/', views.configurar_2fa, name='configurar_2fa'),
    path('seguridad/desactivar-2fa/', views.desactivar_2fa, name='desactivar_2fa'),
    path('seguridad/verificar-2fa/', views.verificar_2fa, name='verificar_2fa'),
    path('generar-qr/<str:qr_url>/', views.generar_qr, name='generar_qr'),
]