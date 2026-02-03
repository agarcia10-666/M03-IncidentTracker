from django.contrib import admin
from .models import SecurityIncident

# Esto hace que el modelo sea visible y editable
admin.site.register(SecurityIncident)

