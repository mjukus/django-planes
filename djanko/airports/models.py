from enum import unique
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
import uuid
# Create your models here.

class Airport(models.Model):
    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    name = models.CharField(max_length=32, unique=True)
    latitude = models.FloatField(validators=[MinValueValidator(-90), MaxValueValidator(90)])
    longitude = models.FloatField(validators=[MinValueValidator(-180), MaxValueValidator(180)])

class Runway(models.Model):
    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    bearing = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(359)])
    length = models.IntegerField(validators=[MinValueValidator(0)])
    unit_choices = [
        ("m","meters"),
        ("ft","feet")
    ]
    length_unit = models.CharField(max_length=2, choices=unit_choices, default="m")
    airport = models.ForeignKey('Airport', on_delete=models.CASCADE, related_name='runways')

class Hangar(models.Model):
    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    airport = models.ForeignKey('Airport', on_delete=models.CASCADE, related_name='hangars')
    spaces = models.PositiveIntegerField()

class PlaneModel(models.Model):
    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    model_number = models.CharField(max_length=10)
    manufacturer = models.CharField(max_length=50)
    fuel_capacity = models.FloatField(validators=[MinValueValidator(0)])
    unit_choices = [
        ("l", "litres"),
        ("gal", "gallons")
    ]
    efficiency_unit_choices = [
        ("mpg", "miles per gallon"),
        ("km/l", "kilometers per litre")
    ]
    fuel_unit = models.CharField(max_length=4, choices=unit_choices, default="l")
    fuel_efficiency = models.PositiveIntegerField()
    efficiency_unit = models.CharField(max_length=4, choices=efficiency_unit_choices, default="mpg")

    def range(self, unit):
        efficiency = self.fuel_efficiency
        if self.efficiency_unit == "mpg":
            #convert to km/l
            efficiency /= 2.35215
        fuel = self.fuel_capacity
        if self.fuel_unit == "gal":
            #convert to lit
            fuel /= 3.78541
        rng = efficiency * fuel
        if unit == "mi":
            #convert to km
            rng /= 1.60934
        return rng

class Plane(models.Model):
    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    plane_number = models.CharField(max_length=10)
    plane_model = models.ForeignKey('PlaneModel', on_delete=models.PROTECT, related_name='planes')
    hangar = models.ForeignKey('Hangar', on_delete=models.SET_NULL, related_name='planes', null=True)