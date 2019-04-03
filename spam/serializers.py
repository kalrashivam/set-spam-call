from rest_framework import serializers
from .models import Spam

class SpamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Spam
        fields = ("phone", "spam", "created_at")
