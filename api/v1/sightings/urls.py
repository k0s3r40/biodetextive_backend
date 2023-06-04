from django.urls import path

from api.v1.sightings.views import SightingApiView, EuropeanaDiscoverApiView, PreviewImageApiView

urlpatterns = [
    path('register-sighting/', SightingApiView.as_view(), name='register-sigthing'),
    path('get-sighting/<int:pk>/', SightingApiView.as_view(), name='get-sigthing'),
    path('get-sightinglist/', SightingApiView.as_view(), name='get-sigthing-list'),
    path('discover/', EuropeanaDiscoverApiView.as_view(), name='discover-list'),
    path('preview-image/<int:pk>/', PreviewImageApiView.as_view(), name='preview-image')
]
