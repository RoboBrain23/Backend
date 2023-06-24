from django.db import models


# Create your models here.


class Chair(models.Model):
    parcode = models.IntegerField(unique=True, db_index=True, null=False)
    password = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        managed = False
        db_table = "chair"

    def __str__(self):
        return f"Chair with ID: {self.parcode}"


class Location(models.Model):
    latitude = models.CharField(max_length=15, null=True, blank=True)
    longitude = models.CharField(max_length=15, null=True, blank=True)

    chair = models.ForeignKey(Chair, models.DO_NOTHING, blank=True, null=True)


class SensorData(models.Model):
    temperature = models.FloatField(blank=True, null=True)
    pulse_rate = models.FloatField(blank=True, null=True)
    oximeter = models.FloatField(blank=True, null=True)
    created_date = models.DateField(blank=True, null=True)
    created_time = models.TimeField(blank=True, null=True)
    chair = models.ForeignKey(Chair, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = "sensor_data"

    def __str__(self):
        return f"This data belongs to chair with ID: {self.chair.pk}"


class Patient(models.Model):
    first_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100, blank=True, null=True)
    gender = models.CharField(max_length=5, blank=True, null=True)
    age = models.IntegerField(blank=True, null=True)
    chair = models.ForeignKey(Chair, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = "patient"

    def __str__(self):
        return f"Patient name: {self.first_name}  {self.last_name}"


class Caregiver(models.Model):
    first_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100, blank=True, null=True)
    username = models.CharField(max_length=100, blank=True, null=True)
    email = models.CharField(max_length=200, blank=True, null=True)
    password = models.CharField(max_length=200, blank=True, null=True)
    age = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "caregiver"

    def __str__(self):
        return f"{self.username}"


class Caregiverphone(models.Model):
    phone_number = models.CharField(max_length=50, blank=True, null=True)
    caregiver = models.ForeignKey(Caregiver, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = "caregiverphone"

    def __str__(self):
        return f"This phone number: {self.phone_number} belongs to {self.caregiver.__str__()}"


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
