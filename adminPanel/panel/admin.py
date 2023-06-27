from django.contrib import admin
from .models import Patient, Chair, Caregiver, Caregiverphone, SensorData, Location
from .forms import ChairAdminForm

# Register your models here.


class PhoneNumberInline(admin.TabularInline):
    model = Caregiverphone
    extra = 0


class CaregiverAdmin(admin.ModelAdmin):
    inlines = [
        PhoneNumberInline,
    ]


class LocationInline(admin.TabularInline):
    model = Location
    extra = 0


class SensorDataInline(admin.TabularInline):
    model = SensorData
    extra = 0


class ChairAdmin(admin.ModelAdmin):
    inlines = [
        LocationInline,
        SensorDataInline,
    ]
    form = ChairAdminForm


admin.site.register(Patient)
admin.site.register(Caregiver, CaregiverAdmin)
admin.site.register(Chair, ChairAdmin)
admin.site.register(SensorData)
