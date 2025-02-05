from django.core.management.base import BaseCommand
from apps.core.models import Camera
from apps.core.stream_manager import StreamManager


class Command(BaseCommand):
    help = 'All streams are running in background FFMPEG process'

    def handle(self, *args, **options):
        cameras = Camera.objects.filter(status=True)
        for camera in cameras:
            StreamManager.start_stream(camera)

        self.stdout.write(self.style.SUCCESS('All streams are running'))
