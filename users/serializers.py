from rest_framework import serializers
from django.contrib.auth import get_user_model

class CustomUserSerializer(serializers.ModelSerializer):
    # def create(self, validated_data):
    #     if validated_data.get('phone')
    #     user = get_user_model().objects.create(**validated_data)

    #     user.save()

    #     return user

    class Meta:
        model = get_user_model()
        fields = ("id", "phone", "name", "email")
