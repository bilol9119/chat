from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import AuthenticationViewSet

urlpatterns = [
    path('token/', AuthenticationViewSet.as_view({"post": "token"})),
    path('token/refresh', TokenRefreshView.as_view()),
    path('register/', AuthenticationViewSet.as_view({"post": "register"}))
]
