# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.


class Video(models.Model):

    youtube_id = models.CharField(max_length=100)
    url = models.URLField(max_length=100)
    audio_filename = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.youtube_id


class User(models.Model):

    video = models.ForeignKey(Video)
    user_email = models.CharField(max_length=100)

    def __str__(self):
        return self.user_email

