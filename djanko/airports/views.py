from django.shortcuts import render
from rest_framework import permissions, generics, views, status
from rest_framework.response import Response
from . import serializers, models
from . import common

# Create your views here.

class AirportList(generics.ListCreateAPIView):
    permission_classes = []#permissions.IsAuthenticated]
    serializer_class = serializers.AirportSerializer
    def get_queryset(self):
        return models.Airport.objects.all()

# class RunwayList(generics.RetrieveAPIView):
#     permission_classes = []#permissions.IsAuthenticated]
#     serializer_class = serializers.AirportRunwaysSerializer
#     def get_queryset(self):
#         return models.Airport.objects.all()

class AirportDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Airport.objects.all()
    lookup_field = 'name'
    permission_classes = []
    serializer_class = serializers.AirportSerializer

    def patch(self, request, *args, **kwargs):
        if "hangar" in request.data:
            if type(request.data["hangar"]) == dict:
                hangarJson = request.data["hangar"]
                hangarSerializer = serializers.HangarSerializer(data=hangarJson)
                hangarSerializer.is_valid(raise_exception=True)
                hangarSerializer.save(airport=self.get_object())
            else:
                try:
                    hangar = models.Hangar.objects.get(id=request.data["hangar"])
                except:
                    return Response("The specified hangar was not found.", status=status.HTTP_400_BAD_REQUEST)
                if hangar in self.get_object().hangars.all():
                    hangar.delete()
                else:
                    Response("The specified hangar is not part of this airport.", status=status.HTTP_400_BAD_REQUEST)
        if "runway" in request.data:
            if type(request.data["runway"]) == dict:
                runwayJson = request.data["runway"]
                runwaySerializer = serializers.RunwaySerializer(data=runwayJson)
                runwaySerializer.is_valid(raise_exception=True)
                runwaySerializer.save(airport=self.get_object())
            else:
                try:
                    runway = models.runway.objects.get(id=request.data["runway"])
                except:
                    return Response("The specified runway was not found.", status=status.HTTP_400_BAD_REQUEST)
                if runway in self.get_object().runways.all():
                    runway.delete()
                else:
                    Response("The specified runway is not part of this airport.", status=status.HTTP_400_BAD_REQUEST)
        return super().patch(request, *args, **kwargs)

# class RunwayDetail(generics.RetrieveUpdateDestroyAPIView):
#     queryset = models.Runway.objects.all()
#     lookup_field = 'id'
#     permission_classes = []
#     serializer_class = serializers.RunwaySerializer

class PlaneModelList(generics.ListCreateAPIView):
    permission_classes = []#permissions.IsAuthenticated]
    serializer_class = serializers.PlaneModelSerializer
    def get_queryset(self):
        return models.PlaneModel.objects.all()

class PlaneList(generics.ListCreateAPIView):
    permission_classes = []#permissions.IsAuthenticated]
    serializer_class = serializers.PlaneSerializer
    def get_queryset(self):
        return models.Plane.objects.all()

class Destinations(generics.RetrieveAPIView):
    permissions_classes = []

    def get(self, request, *args, **kwargs):
        # request = {"plane":3249828934, "origin":342432342354544}
        # response = {"destinations":[,,,,]}
        airports = models.Airport.objects
        try:
            plane = models.Plane.objects.get(id=request.data["plane"])
            origin = airports.get(id=request.data["origin"])
        except KeyError:
            return Response("Must provide an origin & plane uuid.", status=status.HTTP_400_BAD_REQUEST)
        except models.Plane.DoesNotExist:
            return Response("Plane does not match known plane id.", status=status.HTTP_404_NOT_FOUND)
        except models.Airport.DoesNotExist:
            return Response("Airport does not match known airport id.", status=status.HTTP_404_NOT_FOUND)
        planemodel = plane.plane_model
        return common.within_range(origin,
            planemodel.range("km"), airports.all())
