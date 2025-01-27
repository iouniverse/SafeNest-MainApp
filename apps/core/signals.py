import os
import subprocess
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from apps.core.models import Camera


def run_command(command):
    try:
        result = subprocess.run(command, shell=True, check=True, text=True, stderr=subprocess.PIPE)
        return result
    except subprocess.CalledProcessError as e:
        print(f"Command failed: {command}\nError: {e.stderr}")


@receiver(post_save, sender=Camera)
def create_service_file(sender, instance, created, **kwargs):
    if created:
        service_name = f"camera_{instance.id}.service"
        service_path = f"/etc/systemd/system/{service_name}"

        rtsp_url = f"rtsp://{instance.username}:{instance.password}@{instance.ip}:{instance.port}/Streaming/Channels/101"

        output_file = f"/var/lib/streams/camera_{instance.id}_%v.m3u8"

        service_content = f"""
        [Unit]
        Description=FFmpeg stream for Camera {instance.name}
        After=network.target

        [Service]
        ExecStart=/usr/bin/ffmpeg -rtsp_transport tcp -i {rtsp_url} \
            -c:v libx264 -preset ultrafast -tune zerolatency \
            -map 0:v:0 -b:v:0 500k -s:v:0 640x360 \
            -map 0:v:0 -b:v:1 1000k -s:v:1 1280x720 \
            -f hls -hls_time 1 -hls_list_size 3 -hls_flags delete_segments \
            -var_stream_map "v:0,name:low v:1,name:high" {output_file}
        Restart=always

        [Install]
        WantedBy=multi-user.target
        """

        try:
            with open(service_path, "w") as service_file:
                service_file.write(service_content)

            os.chmod(service_path, 0o644)

            run_command("systemctl daemon-reload")
            run_command(f"systemctl enable {service_name}")
            run_command(f"systemctl start {service_name}")

            print(f"Service for camera {instance.name} created and started successfully.")

        except PermissionError:
            print(
                f"Permission denied while creating service file for {instance.name}. Run the script with superuser privileges.")
        except Exception as e:
            print(f"Error while creating service file for {instance.name}: {str(e)}")


@receiver(pre_delete, sender=Camera)
def delete_service_file(sender, instance, **kwargs):
    service_name = f"camera_{instance.id}.service"
    service_path = f"/etc/systemd/system/{service_name}"

    try:
        run_command(f"systemctl stop {service_name}")
        run_command(f"systemctl disable {service_name}")

        if os.path.exists(service_path):
            os.remove(service_path)

        run_command("systemctl daemon-reload")

        print(f"Service for camera {instance.name} deleted successfully.")

    except PermissionError:
        print(
            f"Permission denied while deleting service file for {instance.name}. Run the script with superuser privileges.")
    except Exception as e:
        print(f"Error while deleting service file for {instance.name}: {str(e)}")
