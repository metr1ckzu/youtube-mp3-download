# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import time
import os
from wsgiref.util import FileWrapper

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, FileResponse
from django.core.mail import send_mail
from django.conf import settings

from .models import Video, User
from downloader import tasks

from celery.result import AsyncResult


# Create your views here.

def submit(request):
    template_name = 'downloader/index.html'
    template_name_download = 'downloader/download.html'

    if request.method == 'POST':
        url = request.POST['source_url']
        user_email = request.POST['user_email']

        task = tasks.convert.delay(url)
        result = AsyncResult(task.id)

        is_ready = False
        while not is_ready:
            is_ready = result.ready()
            time.sleep(1)

        data = {
            'task_id': task.id,
            'is_ready': False,
        }

        if result.successful():
            if result.result:
                #youtube_id = result.result['youtube_id']
                filename = result.result['filename']
                download_link = 'http://localhost:8000/download/{}'.format(filename)

                send_mail(
                    'Your video have been converted',
                    'You can download it here {}'.format(download_link),
                    'metr1ckzu@gmail.com',
                    [user_email],
                    fail_silently=False,
                )

        return render(request, template_name_download)
    return render(request, template_name)


def download(request):

    download_url = request.path
    filename = download_url.replace("/download/", "")
    filepath = os.path.join(settings.MEDIA_ROOT, filename)
    response = FileResponse(open(filepath, 'rb'))
    response['Content-Type'] = 'audio/mpeg'
    response['Content-Disposition'] = 'attachment; filename="{}"'.format(filename)
    return response
    close(filepath)
