from django.urls import path
from .views import AddOrderView,ListOrderView


urlpatterns = [
    path('Add/',AddOrderView.as_view(),name="viewOrders" ),
    path('List/',ListOrderView.as_view(),name="viewOrders" ),
    
    ]