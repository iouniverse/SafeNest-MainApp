# import os
# import subprocess
# import time
# import hashlib
# import psutil
#
# STREAMS_FILE = "streams.txt"
# OUTPUT_DIR = "/home/xusandev/Videos"
# CHECK_INTERVAL = 60  # 60 soniyada bir tekshiriladi
#
# # Faol jarayonlar
# active_processes = {}
#
#
# def get_rtsp_streams():
#     """streams.txt faylidan RTSP manzillarni o‘qish"""
#     if not os.path.exists(STREAMS_FILE):
#         return []
#     with open(STREAMS_FILE, "r") as f:
#         return [line.strip() for line in f if line.strip()]
#
#
# def generate_output_filename(rtsp_url):
#     """RTSP manzilidan fayl nomini generatsiya qilish"""
#     stream_hash = hashlib.md5(rtsp_url.encode()).hexdigest()
#     timestamp = time.strftime("%Y-%m-%d_%H-%M-%S")
#     return os.path.join(OUTPUT_DIR, f"{stream_hash}_{timestamp}.mkv")
#
#
# def start_recording(rtsp_url):
#     """FFmpeg orqali RTSP streamni yozishni boshlash"""
#     output_file = generate_output_filename(rtsp_url)
#     command = [
#         "ffmpeg", "-rtsp_transport", "tcp", "-i", rtsp_url,
#         "-c", "copy", output_file
#     ]
#     return subprocess.Popen(command)
#
#
# def stop_process(proc):
#     """FFmpeg jarayonini xavfsiz to‘xtatish"""
#     if proc and proc.pid in psutil.pids():
#         proc.terminate()
#         try:
#             proc.wait(timeout=5)
#         except psutil.TimeoutExpired:
#             proc.kill()
#
#
# while True:
#     new_streams = set(get_rtsp_streams())
#     old_streams = set(active_processes.keys())
#
#     # O‘chirib tashlangan streamlarni to‘xtatish
#     for rtsp in old_streams - new_streams:
#         stop_process(active_processes.pop(rtsp))
#
#     # Yangi streamlarni ishga tushirish
#     for rtsp in new_streams - old_streams:
#         active_processes[rtsp] = start_recording(rtsp)
#
#     time.sleep(CHECK_INTERVAL)
import os
import subprocess
import time
import hashlib
import psutil

STREAMS_FILE = "streams.txt"
OUTPUT_DIR = "/home/user/Videos"
CHECK_INTERVAL = 60
SEGMENT_DURATION = 5

active_processes = {}

# def get_rtsp_streams():
#     if not os.path.exists(STREAMS_FILE):
#         return []
#     with open(STREAMS_FILE, "r") as f:
#         return [line.strip() for line in f if line.strip()]
#
# def generate_output_folder(rtsp_url):
#     stream_hash = hashlib.md5(rtsp_url.encode()).hexdigest()
#     folder_path = os.path.join(OUTPUT_DIR, stream_hash)
#     os.makedirs(folder_path, exist_ok=True)
#     return folder_path
#
# def start_recording(rtsp_url):
#     output_folder = generate_output_folder(rtsp_url)
#     playlist_file = os.path.join(output_folder, "index.m3u8")
#
#     command = [
#         "ffmpeg", "-rtsp_transport", "tcp", "-analyzeduration", "10000000", "-probesize", "10000000",
#         "-i", rtsp_url, "-an", "-c:v", "copy", "-hls_time", str(SEGMENT_DURATION), "-hls_list_size", "10",
#         "-hls_flags", "delete_segments", "-f", "hls", playlist_file
#     ]
#     return subprocess.Popen(command)


# while True:
#     new_streams = set(get_rtsp_streams())
#     print(new_streams)
#     old_streams = set(active_processes.keys())
#
#     for rtsp in old_streams - new_streams:
#         stop_process(active_processes.pop(rtsp))
#
#     for rtsp in new_streams - old_streams:
#         active_processes[rtsp] = start_recording(rtsp)
#
#     time.sleep(CHECK_INTERVAL)
