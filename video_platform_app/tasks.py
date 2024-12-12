import os
import subprocess

RESOLUTIONS = [480, 720, 1080]


def convert(instance):
    for res in RESOLUTIONS:

        source = instance.video.path
        target = f'media/videos/{instance.id}_{instance.title}_{res}p.mp4'.replace(' ', '_')

        cmd = ['ffmpeg', '-i', f'{source}', '-s', f'hd{res}', '-c:v', 'libx264', '-crf', '23', '-c:a', 'aac', '-strict', '-2', f'{target}']

        if not os.path.isdir('logs'):
            subprocess.run(['mkdir', 'logs'], capture_output=True)

        logfile = open("logs/convert.log", "a")

        run = subprocess.run(cmd, capture_output=True)

        to_string = f'{run}'
        formatted_string = to_string.replace('\\n', '\n').replace('\\t', '\t')

        logfile.write(formatted_string)
        logfile.close()


def delete(instance):

    video_path = instance.video.path
    thumbnail_path = instance.thumbnail.path

    if os.path.isfile(thumbnail_path):
        os.remove(thumbnail_path)

    if os.path.isfile(video_path):
        os.remove(video_path)

    for res in RESOLUTIONS:
        converted_video = f'media/videos/{instance.id}_{instance.title}_{res}p.mp4'.replace(' ', '_')
        if os.path.isfile(converted_video):
            os.remove(converted_video)
