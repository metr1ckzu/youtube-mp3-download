# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from .models import Video, User

# Create your views here.

def submit(request):
    template_name = 'downloader/index.html'

    return render(request, template_name)
