from celery import shared_task
from apps.core.models import Camera
from apps.core.stream_manager import StreamManager


@shared_task
def monitor_streams():
    cameras = Camera.objects.filter(status=True)
    for camera in cameras:
        if camera.id not in StreamManager.processes:
            print("Camera is not streaming. Starting...")
            StreamManager.start_stream(camera)

    return True