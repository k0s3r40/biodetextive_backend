from rest_framework.views import APIView
from rest_framework import response
from rest_framework_simplejwt.tokens import RefreshToken

from api.v1.sightings.serializers import SpecimenSightingLimitedSerializer
from api.v1.users.serializers import LoginRegisterSerializer
from specimens.models import SpecimenSighting
from users.models import User


class UserProfile(APIView):
    def get(self, request, *args, **kwargs):
        user_id = str(request.user.id) if request.user.id else None
        sightings = SpecimenSightingLimitedSerializer(
            SpecimenSighting.objects.filter(user=request.user),
            many=True
        ).data
        data = {'user_id': user_id, 'sightings': sightings}
        return response.Response(data, status=200)


class RegisterView(APIView):
    serializer_class = LoginRegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data.get('email')
        password = serializer.validated_data.get('password')

        user = User.objects.create(email=email)
        user.set_password(password)
        user.save()

        refresh = RefreshToken.for_user(user)

        return response.Response(
            {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            },
            status=200
        )
