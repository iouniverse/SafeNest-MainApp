from __future__ import absolute_import, unicode_literals

import os

from celery import Celery

from apps.core.stream_manager import StreamManager

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

app = Celery('config')
app.config_from_object('django.conf:settings', namespace='CELERY')

@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    from apps.core.models import Camera
    cameras = Camera.objects.filter(status=True)
    for camera in cameras:
        StreamManager.start_stream(camera)

app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')