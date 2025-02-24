from django.urls import path
from .views import AddProductView


urlpatterns = [
    path('Add/',AddProductView.as_view(),name="AddProduct" ),
    ]