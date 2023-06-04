from django.urls import path, include

urlpatterns = [
    path('users/', include('api.v1.users.urls')),
    path('sightings/', include('api.v1.sightings.urls')),
]