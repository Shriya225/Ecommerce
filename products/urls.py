from rest_framework.routers import DefaultRouter
from django.urls import path,include
from .views import ProductView,HomeView

router=DefaultRouter()
router.register(r"collections",ProductView,basename="collections")
router.register(r"",HomeView,basename="products")

urlpatterns = [
    path('api/', include(router.urls)),
    path('', include(router.urls)),
 
]
