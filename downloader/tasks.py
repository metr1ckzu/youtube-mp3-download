from __future__ import absolute_import

import os
import shutil
import subprocess
import uuid

form django.conf import settings

from celery import shared_tasks

from youtubeadl.models import Video
from youtubeadl.apps.downloader.utils import create_filename, get_video_info