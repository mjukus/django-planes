from django.urls import path
from django.views.static import serve
from . import views

urlpatterns = [
    path('airports/', views.AirportList.as_view(), name='airport-list'),
    path('airports/<str:name>/', views.AirportDetail.as_view(), name="airport-detail"),
    path('planes/', views.PlaneList.as_view(), name='plane-list'),
    path('plane_models/', views.PlaneModelList.as_view(), name='plane-model-list'),
    path('metrics/destinations/', views.Destinations.as_view(), name='destinations')
]