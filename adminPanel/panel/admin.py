from django.contrib import admin
from .models import Patient, Chair, Caregiver, Caregiverphone, SensorData, Location

# Register your models here.

admin.site.register(Patient)
admin.site.register(Caregiver)
admin.site.register(Caregiverphone)
admin.site.register(Chair)
admin.site.register(SensorData)
admin.site.register(Location)
