from rest_framework import serializers
from . import models, common

class PlaneSerializer(serializers.ModelSerializer):
    within_range = serializers.SerializerMethodField()
    class Meta:
        model = models.Plane
        fields = [
            "id",
            "plane_number",
            "plane_model",
            "hangar",
            "within_range"
        ]

    def get_within_range(self, obj):
        airports = models.Airport.objects
        plane = obj
        if plane.hangar == None:
            origin = models.Airport.objects.first()
            # return []
        else:
            origin = plane.hangar.airport
        planemodel = plane.plane_model
        return [airport.id for airport in common.within_range(origin,
            planemodel.range("km"), airports.all())]

class PlaneModelSerializer(serializers.ModelSerializer):
    planes = serializers.SerializerMethodField()

    class Meta:
        model = models.PlaneModel
        fields = [
            "id",
            "model_number",
            "manufacturer",
            "fuel_capacity",
            "fuel_unit",
            "planes"
        ]
    
    def get_planes(self, obj):
        return [PlaneSerializer(plane).data for plane in obj.planes.all()]

class RunwaySerializer(serializers.ModelSerializer):
    runway_number = serializers.SerializerMethodField()

    class Meta:
        model = models.Runway
        fields = [
            "id",
            "bearing",
            "length",
            "length_unit",
            "runway_number"
        ]

    def get_runway_number(self,obj):
        return "{:03d}".format(obj.bearing)[:2]

class HangarSerializer(serializers.ModelSerializer):
    planes = serializers.SerializerMethodField()

    class Meta:
        model = models.Hangar
        fields = [
            "id",
            "spaces",
            "planes"
        ]
    
    def get_planes(self, obj):
        return [PlaneSerializer(plane).data for plane in obj.planes.all()]

class AirportSerializer(serializers.ModelSerializer):
    runways = serializers.SerializerMethodField()
    hangars = serializers.SerializerMethodField()

    class Meta:
        model = models.Airport
        fields = [
            "id",
            "name",
            "latitude",
            "longitude",
            "runways",
            "hangars"
        ]

    def get_runways(self, obj):
        return [RunwaySerializer(runway).data for runway in obj.runways.all()]
    
    def get_hangars(self, obj):
        return [HangarSerializer(hangar).data for hangar in obj.hangars.all()]
