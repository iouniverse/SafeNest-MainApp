import os
import psutil
import hashlib
import subprocess

from django.conf import settings

OUTPUT_DIR = os.path.join(settings.MEDIA_ROOT, 'streams')
SEGMENT_DURATION = 5


def generate_output_folder(camera_id: str):
    """
    Generates and returns a folder path for storing output based on a unique camera ID.

    This function computes an MD5 hash from the given camera ID to ensure that each
    camera receives a unique and consistent folder for storing output files. It then
    ensures the folder is created in the specified output directory, if it does not
    already exist.

    Args:
        camera_id (str): A unique identifier for the camera.

    Returns:
        str: The absolute path of the generated folder where output files can be stored.
    """
    stream_hash = hashlib.md5(camera_id.encode()).hexdigest()
    folder_path = os.path.join(OUTPUT_DIR, stream_hash)
    os.makedirs(folder_path, exist_ok=True)
    return folder_path


def is_stream_running(camera_id: str):
    """
    Checks if a media stream is currently running based on the given camera ID.

    This function determines if a stream is currently active by checking
    for the existence of the corresponding playlist file and also verifying
    whether an associated ffmpeg process is running. It computes a hashed
    unique identifier for the camera using the provided `camera_id` and
    checks specific system processes to ascertain if a stream linked to
    that identifier is active.

    Parameters:
    camera_id: str
        The unique identifier of the camera for which the stream status
        needs to be checked.

    Returns:
    bool
        True if a stream is running for the given camera ID, otherwise False.
    """
    stream_hash = hashlib.md5(camera_id.encode()).hexdigest()
    output_folder = os.path.join(OUTPUT_DIR, stream_hash)
    playlist_file = os.path.join(output_folder, "index.m3u8")

    if not os.path.exists(playlist_file):
        return False

    for process in psutil.process_iter(attrs=['pid', 'name', 'cmdline']):
        try:
            cmdline = process.info.get("cmdline", [])
            if cmdline and "ffmpeg" in process.info["name"] and any(stream_hash in arg for arg in cmdline):
                return True

        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            continue

    return False


def record_camera_stream(rtsp_url, camera_id):
    """
    Records the live RTSP camera stream to an HLS format playlist.

    This function checks if a stream is already running for the provided camera ID.
    If the stream is running, it generates a hash for the camera ID and returns the
    stream's HLS playlist URL. If not, it initiates a new recording process, uses
    FFmpeg to capture the stream in HLS format, and returns the path to the newly
    created playlist.

    Arguments:
        rtsp_url : str
            The RTSP URL of the camera stream.
        camera_id : int
            The unique identifier of the camera for which the stream is recorded.

    Returns:
        str
            The URL or file path for the created HLS playlist.
    """
    if is_stream_running(str(camera_id)):
        stream_hash = hashlib.md5(str(camera_id).encode()).hexdigest()
        return f"{settings.MEDIA_URL}streams/{stream_hash}/index.m3u8"

    output_folder = generate_output_folder(str(camera_id))
    playlist_file = os.path.join(output_folder, "index.m3u8")

    # command = [
    #     "ffmpeg", "-rtsp_transport", "tcp", "-analyzeduration", "10000000", "-probesize", "10000000",
    #     "-i", rtsp_url, "-an", "-c:v", "copy", "-hls_time", str(SEGMENT_DURATION), "-hls_list_size", "10",
    #     "-hls_flags", "delete_segments", "-f", "hls", playlist_file
    # ]
    command = [
        "ffmpeg", "-rtsp_transport", "tcp", "-analyzeduration", "10000000", "-probesize", "10000000",
        "-i", rtsp_url, "-c:v", "copy", "-c:a", "aac", "-hls_time", str(SEGMENT_DURATION), "-hls_list_size", "10",
        "-hls_flags", "delete_segments", "-f", "hls", playlist_file
    ]

    try:
        subprocess.Popen(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except Exception as e:
        print(f"Failed to start ffmpeg: {e}")

    return f"{output_folder}/index.m3u8"


def stop_process(proc):
    """
    Stops a specified process safely by first attempting to terminate it. If the process
    fails to terminate within a specified timeout, it will be forcefully killed.

    Args:
        proc (psutil.Process): The process object to be stopped. If the process is
        None or its PID is not present in the list of active PIDs, the function
        does nothing.

    Raises:
        psutil.TimeoutExpired: If the process fails to stop after attempting to
        terminate it and before calling kill.
    """
    if proc and proc.pid in psutil.pids():
        proc.terminate()
        try:
            proc.wait(timeout=5)
        except psutil.TimeoutExpired:
            proc.kill()
