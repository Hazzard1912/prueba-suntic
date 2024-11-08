from django.urls import path
from . import views

app_name = 'documents'

urlpatterns = [
    path('', views.document_list, name='document_list'),
    path('<int:pk>/', views.document_detail, name='document_detail'),
    path('create/', views.document_create, name='document_create'),
    path('<int:pk>/edit/', views.document_edit, name='document_edit'),
    path('<int:pk>/delete/', views.document_delete, name='document_delete'),
    path('<int:pk>/approve/', views.document_approve, name='document_approve'),
    path('<int:pk>/preview/', views.document_preview, name='document_preview'),
]
