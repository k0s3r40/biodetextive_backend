from django.urls import path
from rest_framework_simplejwt import views as jwt_views

from api.v1.users.views import RegisterView, UserProfile

urlpatterns = [
    path('login/', jwt_views.TokenObtainPairView.as_view(), name='login'),
    path('refresh/', jwt_views.TokenRefreshView.as_view(), name='refresh_token'),
    path('register/', RegisterView.as_view(), name='register'),
    path('user/', UserProfile.as_view(), name='user_profile'),
]