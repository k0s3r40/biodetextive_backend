from rest_framework import serializers

from specimens.models import Specimen, SpecimenSighting


class ProcessSightingSerializer(serializers.Serializer):
    image = serializers.CharField(required=True)
    lat = serializers.DecimalField(required=True, max_digits=9,decimal_places=7)
    lon = serializers.DecimalField(required=True, max_digits=9,decimal_places=7)


class SpecimenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Specimen
        fields = ['name', 'description']


class SpecimenSightingSerializer(serializers.ModelSerializer):
    specimen = SpecimenSerializer(read_only=True)

    class Meta:
        model = SpecimenSighting
        fields = ['specimen', 'image','latitude', 'longitude', 'timestamp', 'europeana_data']

class SpecimenSightingLimitedSerializerWithImage(SpecimenSightingSerializer):
    image_url = serializers.CharField(required=True)
    class Meta:
        model = SpecimenSighting
        fields = ['specimen', 'id', 'image_url']
class SpecimenSightingLimitedSerializer(SpecimenSightingSerializer):
    class Meta:
        model = SpecimenSighting
        fields = ['specimen', 'id']