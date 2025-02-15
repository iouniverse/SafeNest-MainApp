from celery import shared_task
from apps.core.models import Camera
from apps.core.stream_manager import StreamManager


@shared_task
def create_camera_and_start_stream(camera_id):
    print(f"Received task to start stream for Camera ID: {camera_id}")
    try:
        camera = Camera.objects.get(id=camera_id)
        print(f"Camera found: {camera}")
        StreamManager.start_stream(camera)
        print("Stream started successfully!")
    except Camera.DoesNotExist:
        print(f"Camera with ID {camera_id} does not exist")
    except Exception as e:
        print(f"Error while starting stream: {e}")