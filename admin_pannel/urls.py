from django.urls import path
from .views import AddProductView,ListProductView,DeleteProductView


urlpatterns = [
    path('Add/',AddProductView.as_view(),name="AddProduct" ),
    path('List/',ListProductView.as_view()),
    path('Delete/',DeleteProductView.as_view()),
    path('ViewOrders/',DeleteProductView.as_view()),
    ]