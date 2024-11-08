from django.db import models

class Document(models.Model):
    STATUS_CHOICES = (
        ('pendiente', 'Pendiente'),
        ('aprobado', 'Aprobado'),
        ('rechazado', 'Rechazado'),
    )
    
    titulo = models.CharField(max_length=255)
    descripcion = models.TextField()
    path = models.FileField(upload_to='documents/')
    owner = models.ForeignKey('custom_auth.User', on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pendiente')
    approver = models.ForeignKey('custom_auth.User', on_delete=models.SET_NULL, null=True, blank=True, related_name='approver')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.titulo
    