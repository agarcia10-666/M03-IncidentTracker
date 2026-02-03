from django.db import models

class SecurityIncident(models.Model):
    # Definimos las opciones para la severidad
    SEVERITY_CHOICES = [
        ('Baja', 'Baja'),
        ('Media', 'Media'),
        ('Alta', 'Alta'),
    ]
    
    title = models.CharField(max_length=200)       # Título corto
    description = models.TextField()                # Descripción larga
    severity = models.CharField(                    # Desplegable con las opciones
        max_length=10, 
        choices=SEVERITY_CHOICES, 
        default='Media'
    )
    detected_at = models.DateTimeField(auto_now_add=True) # Fecha automática

    def __str__(self):
        return self.title
