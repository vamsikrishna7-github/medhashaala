from django.urls import path
from .views import CustomTokenObtainPairView

urlpatterns = [
    path('jwt/create/', CustomTokenObtainPairView.as_view(), name='jwt-create'),
]


