from django.urls import path
from .views import RegisterUserView,logout,ProfileView
# from rest_framework_simplejwt.views import(TokenObtainPairView,TokenRefreshView)
from .views import RegisterUserView, logout, ProfileView, CustomTokenObtainPairView, CustomTokenRefreshView,AdminTokenObtainPairView,AdminTokenRefreshView,admin_logout

urlpatterns = [
 path("api/register/",RegisterUserView.as_view(),name="RegisterView"),
#  path("api/login/",TokenObtainPairView.as_view()),
#  path("api/refresh/",TokenRefreshView.as_view()),
 path("api/login/", CustomTokenObtainPairView.as_view(), name="token_obtain_pair"),
 path("api/refresh-user/", CustomTokenRefreshView.as_view(), name="token_refresh_user"),
 path("api/logout-user/",logout),
 path("api/logout-admin/",admin_logout),
 path("api/profile/",ProfileView.as_view()),
 path("api/admin-login/", AdminTokenObtainPairView.as_view(), name="admin_token_obtain_pair"),
  path('api/refresh-admin/', AdminTokenRefreshView.as_view(), name='admin-refresh'),
]

