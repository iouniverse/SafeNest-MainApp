import os
import subprocess

from django.conf import settings


class StreamManager:
    processes = {}

    @staticmethod
    def get_rtsp_url(camera: object) -> object:
        """
        Create RTSP URL
        """
        return f"rtsp://{camera.username}:{camera.password}@{camera.ip}:{camera.port}/Streaming/Channels/101"

    @staticmethod
    def start_stream(camera: object):
        """
        Start streaming camera and save process
        """
        if camera.id in StreamManager.processes:
            """
            Camera is already streaming
            """
            return

        rtsp_url = StreamManager.get_rtsp_url(camera)
        output_file = os.path.join(settings.MEDIA_ROOT, f"cameras/camera_{camera.id}_%v.m3u8")

        command = [
            "ffmpeg", "-rtsp_transport", "tcp", "-i", rtsp_url,
            "-c:v", "libx264", "-preset", "fast", "-tune", "film",
            "-map", "0:v:0", "-b:v:0", "500k", "-s:v:0", "640x360",
            "-map", "0:v:0", "-b:v:1", "1000k", "-s:v:1", "1280x720",
            "-fflags", "nobuffer", "-flush_packets", "1",
            "-f", "hls", "-hls_time", "5", "-hls_list_size", "10", "-hls_flags", "append_list,delete_segments",
            "-var_stream_map", "v:0,name:low v:1,name:high", output_file
        ]

        process = subprocess.Popen(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        StreamManager.processes[camera.id] = process

        print(f"Camera {camera.id} started streaming")

    @staticmethod
    def stop_stream(camera_id):
        """
        Camera is not streaming
        """
        if camera_id in StreamManager.processes:
            StreamManager.processes[camera_id].terminate()
            del StreamManager.processes[camera_id]

            print(f"Camera {camera_id} stopped streaming")

    @staticmethod
    def restart_stream(camera):
        """
        Camera is streaming, restart it
        """
        StreamManager.stop_stream(camera.id)
        StreamManager.start_stream(camera)
