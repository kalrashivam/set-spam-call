# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from .serializers import SpamSerializer
from .models import Spam


class SpamView(ModelViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = SpamSerializer

    def get_queryset(self):
        return self.request.user.spam_set.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
