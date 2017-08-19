# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import time

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.core.mail import send_mail
from django.core.urlresolvers import reverse

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
                youtube_id = result.result['youtube_id']
                filename = result.result['filename']
                download_link = reverse(
                    'download_view',
                    kwargs={'youtube_id': youtube_id,
                            'filename': filename})

                send_mail(
                    'Your video have been converted',
                    'You can download it here {}'.format(download_link),
                    'metr1ckzu@gmail.com',
                    [user_email],
                    fail_silently=false,
                )

        return render(request, template_name_download)
    return render(request, template_name)

def download(request, youtube_id, filename):

    filepath = os.path.join(settings.MEDIA_ROOT, filename)
    file_exists = os.path.exist(filepath)

    video = None

    try:
        video = Video.objects.get(youtube_id=youtube_id, audio_filename=filename)
    except Video.DoesNotExist:
        pass

    if video and file_exists:
        response = HttpResponse(content_type='application/force_download')
        response['Content-Length'] = os.path.getsize(filepath)
        response
