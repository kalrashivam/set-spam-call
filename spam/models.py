# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth import get_user_model


class Spam(models.Model):
    user = models.ForeignKey(
        get_user_model(), on_delete=models.SET_NULL, null=True)
    phone = models.CharField(max_length=10)
    spam = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "{name} reported {phone} as {spam}spam".format(
            name=self.user and self.user.name or 'Deleted User',
            phone=self.phone,
            spam='' if self.spam else 'not '
        )
