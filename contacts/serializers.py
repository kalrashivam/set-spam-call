from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Contact

class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = ("phone", "name", "created_at")
