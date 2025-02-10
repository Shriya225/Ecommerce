from rest_framework.routers import DefaultRouter
from django.urls import path,include
from .views import ViewCart,AddCart,UpdateCartView,DeleteCartItemView

urlpatterns = [
    path('ListCart/',ViewCart.as_view(),name="viewCart" ),
    path('addCart/',AddCart.as_view(),name="addCart"),
    path('updateCart/',UpdateCartView.as_view(),name="UpdateCart"),
    path('deleteCartItem/',DeleteCartItemView.as_view(),name="deleteCartItem"),
 
]