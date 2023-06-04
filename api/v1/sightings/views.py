from django.http import HttpResponse, FileResponse
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework import response
from api.v1.sightings.serializers import (
    ProcessSightingSerializer,
    SpecimenSightingSerializer,
    SpecimenSightingLimitedSerializerWithImage
)
from specimens.analyze_image import analyze_image_with_cloud_vision
from specimens.europeana_communication import get_data_from_europeana
from specimens.models import Specimen, SpecimenSighting
from specimens.open_api_communication import get_openai_data
from django.utils import timezone
import io


class EuropeanaDiscoverApiView(APIView):
    def get(self, request, *args, **kwargs):
        lat = float(request.GET.get('lat'))
        lon = float(request.GET.get('lon'))
        data = get_data_from_europeana(lat=lat, lon=lon, only_one=False)
        return response.Response(data, status=200)


class PreviewImageApiView(APIView):
    def get(self, request, pk, *args, **kwargs):
        sighting = get_object_or_404(SpecimenSighting, pk=pk)
        img = sighting.get_image
        img_io = io.BytesIO()
        img.save(img_io, format='JPEG')
        img_io.seek(0)
        return HttpResponse(img_io, content_type='image/jpeg')


class SightingApiView(APIView):
    serializer_class = ProcessSightingSerializer

    def get(self, request, pk=None, *args, **kwargs):
        if not pk:
            sightings = SpecimenSighting.objects.filter(user=request.user).order_by('-id')[:20]
            data = SpecimenSightingLimitedSerializerWithImage(sightings, many=True).data
            return response.Response(data, status=200)
        sighting = get_object_or_404(SpecimenSighting, pk=pk, user=request.user)
        data = SpecimenSightingSerializer(sighting).data
        return response.Response(data, status=201)

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        image = serializer.validated_data.get('image')
        title = analyze_image_with_cloud_vision(image)
        description = get_openai_data([{'role': 'user', 'content': f"Give me a short description of {title} up to 50 words."}])
        category = get_openai_data([{'role': 'user', 'content': f"In one word, what is '{title}'? {','.join(i[0] for i in Specimen.SPECIMEN_CATEGORIES)}"}])
        specimen = Specimen.objects.filter(name=title).first()
        if not specimen:
            specimen = Specimen.objects.create(name=title, description=description, category=category)
        lat = float(serializer.validated_data.get('lat'))
        lon = float(serializer.validated_data.get('lon'))
        europeana_data = get_data_from_europeana(lat, lon)
        specimen_sighting = SpecimenSighting.objects.create(
            user=request.user,
            specimen=specimen,
            image=image,
            latitude=lat,
            longitude=lon,
            timestamp=timezone.now(),
            europeana_data=europeana_data
        )
        return response.Response(SpecimenSightingSerializer(specimen_sighting).data, status=201)
