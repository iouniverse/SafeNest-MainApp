import os
import subprocess
import logging
import threading
from django.conf import settings

class StreamManager:
    processes = {}

    @staticmethod
    def get_rtsp_url(camera):
        """
        Create RTSP URL
        """
        return f"rtsp://{camera.username}:{camera.password}@{camera.ip}:{camera.port}/Streaming/Channels/101"

    @staticmethod
    def start_stream(camera):
        """
        Start streaming camera in a separate thread.
        """
        logger = logging.getLogger(__name__)

        if camera.id in StreamManager.processes:
            logger.info(f"Camera {camera.id} is already streaming")
            return

        def run_stream():
            rtsp_url = StreamManager.get_rtsp_url(camera)
            output_file = os.path.join(settings.MEDIA_ROOT, f"cameras/camera_{camera.id}_%v.m3u8")

            command = [
                "ffmpeg", "-rtsp_transport", "tcp", "-i", rtsp_url,
                "-c:v", "libx264", "-preset", "ultrafast", "-tune", "zerolatency",
                "-maxrate", "1000k", "-bufsize", "2000k", "-pix_fmt", "yuv420p",
                "-map", "0:v:0", "-b:v:0", "500k", "-s:v:0", "640x360",
                "-map", "0:v:0", "-b:v:1", "1000k", "-s:v:1", "1280x720",
                "-f", "hls", "-hls_time", "2", "-hls_list_size", "4",
                "-hls_flags", "delete_segments", "-var_stream_map", "v:0,name:low v:1,name:high",
                output_file
            ]

            try:
                process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                StreamManager.processes[camera.id] = process

                logger.info(f"Camera {camera.id} started streaming")
                print(f"Camera {camera.id} started streaming")

                process.wait()

            except Exception as e:
                logger.error(f"Error starting stream for camera {camera.id}: {str(e)}")
                print(f"Error starting stream for camera {camera.id}: {str(e)}")

        thread = threading.Thread(target=run_stream, daemon=True)
        thread.start()

    @staticmethod
    def stop_stream(camera_id):
        """
        Stop streaming camera
        """
        logger = logging.getLogger(__name__)

        if camera_id in StreamManager.processes:
            StreamManager.processes[camera_id].terminate()
            del StreamManager.processes[camera_id]

            logger.info(f"Camera {camera_id} stopped streaming")
            print(f"Camera {camera_id} stopped streaming")
        else:
            logger.warning(f"Camera {camera_id} is not streaming")

    @staticmethod
    def restart_stream(camera):
        """
        Restart the streaming process
        """
        logger = logging.getLogger(__name__)

        logger.info(f"Restarting stream for camera {camera.id}")
        StreamManager.stop_stream(camera.id)
        StreamManager.start_stream(camera)
