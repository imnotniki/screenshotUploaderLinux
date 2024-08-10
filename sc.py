import os
import PIL.ImageGrab
import time
import paramiko
import pyperclip
import json
import subprocess

settings = {}

def load_settings():
    global settings
    if os.path.exists("/home/shana/PycharmProjects/shananikiScreenshot/settings.json"):
        with open("/home/shana/PycharmProjects/shananikiScreenshot/settings.json", "r") as f:
            settings = json.load(f)

def upload_to_ftp(file_path):
    try:
        ftp_server = settings.get("ftp_server", "")
        ftp_username = settings.get("ftp_username", "")
        ftp_port = settings.get("ftp_port", "")
        ftp_password = settings.get("ftp_password", "")
        url = settings.get("url", "")
        upload_path = settings.get("upload_path", "")

        # Create an SSH client
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(ftp_server, int(ftp_port), ftp_username, ftp_password)

        # Open an SFTP session
        sftp = ssh.open_sftp()

        # Upload the file
        remote_path = upload_path + os.path.basename(file_path)
        sftp.put(file_path, remote_path)

        sftp.close()
        ssh.close()
        dest_url = url + os.path.basename(file_path)
        pyperclip.copy(dest_url)
    except Exception as e:
        print(e)
        exit(0)

if __name__ == "__main__":
    load_settings()
    result = subprocess.run(['xrectsel'], capture_output=True, text=True)
    start_x = int(result.stdout.split('+')[1].split('+')[0])
    start_y = int(result.stdout.split('+')[2])
    end_x = start_x + int(result.stdout.split('x')[0])
    end_y = start_y + int(result.stdout.split('x')[1].split('+')[0])
    box = (start_x, start_y, end_x, end_y)
    img = PIL.ImageGrab.grab(bbox=box)
    name = str(time.strftime('%Y%m%D%H%S').replace('/', '')) + ".png"
    img.save(name)
    upload_to_ftp(name)
    os.remove(name)