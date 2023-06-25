# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Association(models.Model):
    patient = models.ForeignKey(
        "Patient", models.DO_NOTHING, db_column="patient", blank=True, null=True
    )
    caregiver = models.ForeignKey(
        "Caregiver", models.DO_NOTHING, db_column="caregiver", blank=True, null=True
    )

    class Meta:
        managed = False
        db_table = "association"


class Caregiver(models.Model):
    first_name = models.CharField(max_length=50, blank=True, null=True)
    last_name = models.CharField(max_length=50, blank=True, null=True)
    username = models.CharField(max_length=150, blank=True, null=True)
    email = models.CharField(max_length=150, blank=True, null=True)
    password = models.CharField(max_length=250, blank=True, null=True)
    age = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "caregiver"

    def __str__(self):
        return f"{self.username}"


class Caregiverphone(models.Model):
    phone_number = models.CharField(max_length=25, blank=True, null=True)
    caregiver = models.ForeignKey(Caregiver, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = "caregiverphone"

    def __str__(self):
        return f"This phone number: {self.phone_number} belongs to {self.caregiver.__str__()}"


class Chair(models.Model):
    parcode = models.IntegerField(unique=True, blank=True, null=True)
    password = models.CharField(max_length=250)
    available = models.BooleanField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "chair"

    def __str__(self):
        return f"Chair with ID: {self.parcode}"


class Location(models.Model):
    latitude = models.DecimalField(
        max_digits=9, decimal_places=6, blank=True, null=True
    )
    longitude = models.DecimalField(
        max_digits=9, decimal_places=6, blank=True, null=True
    )
    chair = models.ForeignKey(Chair, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = "location"


class Patient(models.Model):
    first_name = models.CharField(max_length=50, blank=True, null=True)
    last_name = models.CharField(max_length=50, blank=True, null=True)
    gender = models.CharField(max_length=5, blank=True, null=True)
    age = models.IntegerField(blank=True, null=True)
    chair = models.ForeignKey(Chair, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = "patient"

    def __str__(self):
        return f"Patient name: {self.first_name}  {self.last_name}"


class SensorData(models.Model):
    temperature = models.FloatField()
    pulse_rate = models.FloatField()
    oximeter = models.FloatField()
    created_date = models.DateField(blank=True, null=True)
    created_time = models.TimeField(blank=True, null=True)
    chair = models.ForeignKey(Chair, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = "sensor_data"

    def __str__(self):
        return f"This data belongs to chair with ID: {self.chair.pk}"
