from urllib import parse

from django.http import HttpResponse, FileResponse
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework import response
from api.v1.sightings.serializers import (
    ProcessSightingSerializer,
    SpecimenSightingSerializer,
    SpecimenSightingLimitedSerializerWithImage
)
import requests
from specimens.analyze_image import analyze_image_with_cloud_vision
from specimens.europeana_communication import get_data_from_europeana
from specimens.models import Specimen, SpecimenSighting
from specimens.open_api_communication import get_openai_data
from django.utils import timezone
import io
from django.conf import settings


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
        google_response = requests.get(f'https://customsearch.googleapis.com/customsearch/v1?cx=001928687561571394193%3At_qhgoibaiq&num=2&q={parse.quote(title)}%20description&key={settings.GOOGLE_API_KEY}')
        description = get_openai_data(
            [{'role': 'user', 'content': f"A person took a picture of a {title} google returned {google_response.json()}, extract the description from here and summarize it up to 50 words I need description of the thing. Take the risk no explanations just the description."}])
        category = get_openai_data([{'role': 'user', 'content': f"In one word, what is '{title}'? Choose from and dont add additives like dots or sth {','.join(i[0] for i in Specimen.SPECIMEN_CATEGORIES)}"}]).strip('.! ')
        specimen_class = get_openai_data([{'role': 'user', 'content': f"In one word, rate the rarity of seeing '{title}'? {','.join(i[0] for i in Specimen.SPECIMEN_CLASSES)}"}])
        specimen = Specimen.objects.filter(name=title).first()
        if not specimen:
            specimen = Specimen.objects.create(name=title.strip('\"\''), specimen_class=specimen_class.strip('.').strip(' '), description=description, category=category.strip('.!'))
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
