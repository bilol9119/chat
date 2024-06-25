from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import AuthenticationViewSet, UserViewSet

urlpatterns = [
    path('token/', AuthenticationViewSet.as_view({"post": "token"})),
    path('token/refresh/', TokenRefreshView.as_view()),
    path('register/', AuthenticationViewSet.as_view({"post": "register"})),
    path('register/verify/', AuthenticationViewSet.as_view({"post": "verify_register"})),
    path('auth/me/', UserViewSet.as_view({"get": "auth_me"})),
    path('profile/update/', UserViewSet.as_view({"patch": "profile_update"})),
    path('users/<str:username>/', UserViewSet.as_view({"get": "get_user"})),
]
