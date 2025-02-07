from rest_framework.routers import DefaultRouter
from django.urls import path,include
from .views import ViewCart,AddCart

urlpatterns = [
    path('',ViewCart.as_view(),name="viewCart" ),
    path('addCart/',AddCart.as_view(),name="addCart"),
 
]