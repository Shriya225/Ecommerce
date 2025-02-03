from rest_framework.routers import DefaultRouter
from django.urls import path,include
from .views import ProductView

router=DefaultRouter()
router.register(r"collections",ProductView,basename="collections")

urlpatterns = [
    path('api/', include(router.urls)),
]