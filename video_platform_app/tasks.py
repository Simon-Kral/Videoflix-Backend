import os
import shutil
import shlex
import subprocess
import json
from django_rq import job
from .models import Video


RESOLUTIONS = [
    {'width': 640, 'height': 360, 'max_bitrate_video': 1500, 'max_bitrate_audio': 64},
    {'width': 854, 'height': 480, 'max_bitrate_video': 4000, 'max_bitrate_audio': 128},
    {'width': 1280, 'height': 720, 'max_bitrate_video': 7500, 'max_bitrate_audio': 128},
    {'width': 1920, 'height': 1080, 'max_bitrate_video': 12000, 'max_bitrate_audio': 192},
]


def convert(instance):

    convert_to_hls(instance)

    if not instance.thumbnail:
        convert_to_png(instance)


def convert_to_hls(instance):

    convert_cmd = create_hls_command(instance)
    subprocess.run(convert_cmd, check=True)


def create_hls_command(instance):
    source = instance.video.path
    target = create_hls_target(instance)
    orig_resolution = get_resolution(source)

    cmd = get_initial_command_block(source)

    cmd = add_resolution_maps(cmd, orig_resolution)

    cmd = add_map_filters(cmd, orig_resolution)

    cmd = add_stream_map(cmd, orig_resolution)

    cmd = add_final_command_block(cmd, target)

    return cmd


def create_hls_target(instance):
    target_folder = f'/home/monti/Dev/Backend/media/videos/{instance.id}_{instance.title}'.replace(' ', '_')
    os.makedirs(target_folder, exist_ok=True)
    target_file = f'{instance.id}_{instance.title}_%v.m3u8'.replace(' ', '_')
    target = os.path.join(target_folder, target_file)
    return target


def get_initial_command_block(source):

    initial_command_block = [
        'ffmpeg',
        '-hwaccel', 'cuda',
        '-i', f'{source}',
        '-c:v', 'h264_nvenc',
        '-c:a', 'aac',
        '-ar', '48000',
    ]

    return initial_command_block


def add_resolution_maps(cmd, orig_resolution):

    for res in RESOLUTIONS:
        if res['height'] <= orig_resolution:
            cmd.extend(['-map', '0:v:0', '-map', '0:a:0'])

    return cmd


def add_map_filters(cmd, orig_resolution):

    for idx, res in enumerate(RESOLUTIONS):
        if res['height'] <= orig_resolution:
            cmd.extend([f'-filter:v:{idx}', f'scale=w={res['width']}:h={res['height']}', f'-maxrate:v:{idx}', f'{res['max_bitrate_video']}k', '-b:a:0', f'{res['max_bitrate_audio']}k'])

    return cmd


def add_stream_map(cmd, orig_resolution):

    cmd.append('-var_stream_map')
    stream_map = []

    for idx, res in enumerate(RESOLUTIONS):
        if res['height'] <= orig_resolution:
            stream_item = f'v:{idx},a:{idx},name:{res['height']}p'
            stream_map.append(stream_item)

    cmd.append(' '.join(stream_map))

    return cmd


def add_final_command_block(cmd, target):

    final_command_block = [
        '-preset', 'slow',
        '-hls_list_size', '0',
        '-threads', '0',
        '-f', 'hls',
        '-hls_playlist_type', 'event',
        '-hls_time', '3',
        '-hls_flags', 'independent_segments',
        '-master_pl_name', 'playlist.m3u8',
        f'{target}'
    ]

    cmd.extend(final_command_block)

    return cmd


def convert_to_png(instance):
    source = instance.video.path
    target = f'thumbnails/{instance.id}_{instance.title}.png'.replace(' ', '_')
    orig_duration = get_duration(source)
    timestamp = orig_duration / 2

    cmd = f'ffmpeg -i {source} -f mjpeg -ss {timestamp} -vframes 1 -y media/{target}'.split()
    subprocess.run(cmd, check=True)

    instance.thumbnail = target
    instance.save()


def get_duration(source):
    duration_cmd = f'ffprobe -v error -show_entries format=duration -of default=nw=1:nk=1 {source}'
    result = subprocess.getoutput(duration_cmd)
    formatted_result = format_ffprobe_result(result)
    return formatted_result


def get_resolution(source):
    resolution_cmd = f'ffprobe -v error -select_streams v:0 -show_entries stream=height -of default=nw=1:nk=1 {source}'
    result = subprocess.getoutput(resolution_cmd)
    formatted_result = format_ffprobe_result(result)
    return formatted_result


def format_ffprobe_result(result):
    formatted_result = int(float(result))
    return formatted_result


def delete(instance):

    if instance.thumbnail and os.path.isfile(instance.thumbnail.path):
        os.remove(instance.thumbnail.path)

    if instance.video and os.path.isfile(instance.video.path):
        os.remove(instance.video.path)

    if os.path.isdir(f'media/videos/{instance.id}_{instance.title.replace(' ', '_')}'):
        shutil.rmtree(f'media/videos/{instance.id}_{instance.title.replace(' ', '_')}')


# def convert_to_hls(instance):
#     source = instance.video.path
#     orig_resolution = get_resolution(source)
#     for res in RESOLUTIONS:
#         if res['height'] <= orig_resolution:
#             try:
#                 target = create_hls_target(instance, res)
#                 convert_cmd = create_hls_command(source, target, res)
#                 subprocess.run(convert_cmd, check=True)
#             except:
#                 print('an error occurred')

# def create_hls_target(instance, res):
#     target_path = f'/home/monti/Dev/Backend/media/videos/{instance.id}_{instance.title}/{res['height']}p'.replace(' ', '_')
#     os.makedirs(target_path, exist_ok=True)
#     target_file = f'playlist.m3u8'
#     return os.path.join(target_path, target_file)


# def create_hls_command(source, target, res):

    # cmd = f'
    # ffmpeg
    # -hwaccel cuda
    # -i {source}
    # -vf scale={res['width']}:{res['height']}
    # -b:v {res['bitrate']}k
    # -b:a 192k
    # -c:v h264_nvenc
    # -c:a aac
    # -f hls
    # -hls_time 3
    # -hls_playlist_type vod
    # -y
    # {target}
    # '.split()

#     return cmd
