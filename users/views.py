from django.contrib.auth import get_user_model
from django.db import IntegrityError

from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .serializers import CustomUserSerializer


class CreateUserView(
    GenericViewSet
):
    serializer_class = CustomUserSerializer

    def create(self, request):

        if any([key not in request.data for key in ['name', 'phone']]):
            return Response({'error': 'Missing params '}, status.HTTP_400_BAD_REQUEST)

        name = request.data.get('name')
        phone = request.data.get('phone')

        if len(phone) < 10 or not phone.isdigit():
            return Response({'error': 'Invalid phone number'}, status.HTTP_400_BAD_REQUEST)

        if len(name) < 2 or name.isdigit():
            return Response({'error': 'Invalid name'}, status.HTTP_400_BAD_REQUEST)

        try:
            user = get_user_model().objects.create(
                name=name,
                phone=phone,
                email=request.data.get('email', None)
            )

            user.set_password(request.data.get('password'))
            user.save()

            return Response(self.get_serializer(user).data)
        except IntegrityError:
            return Response({'error': 'User with phone number already exists'}, status.HTTP_400_BAD_REQUEST)


class UserView(
    mixins.UpdateModelMixin,
    GenericViewSet
):
    permission_classes = (IsAuthenticated,)
    serializer_class = CustomUserSerializer
    queryset = get_user_model().objects.all()

    def get_object(self):
        return self.request.user

    def list(self, request, pk=None):
        return Response(self.get_serializer(request.user).data)
