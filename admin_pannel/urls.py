from django.urls import path
from .views import AddProductView,ListProductView,DeleteProductView,ListOrderView


urlpatterns = [
    path('Add/',AddProductView.as_view(),name="AddProduct" ),
    path('List/',ListProductView.as_view()),
    path('Delete/',DeleteProductView.as_view()),
    path('ViewOrders/',ListOrderView.as_view()),
    ]
