import os
from os import listdir
from os.path import isfile, join
import subprocess
import time

# TODO try on windows!!!


#directory_path = '/media/pi/toshiba/test'
directory_path_unconverted = '/home/pi/Desktop/'
directory_path_converted = '/home/pi/Desktop/converted/'

#available_files = [f for f in listdir(directory_path) if isfile(join(directory_path, f))]


# converts from mp4 to mp4 - which somehow fixes playing issues with mp4 files created in windows
def convert_video(video):
    video_file_format = video[-4:]
    video_name = video[:-4]

    video_path_unconverted = directory_path_unconverted + video
    video_path_converted = directory_path_converted + video_name + '.h264'
    
    # convert video if not converted yet
    if not os.path.exists(video_path_converted):
        try:
            cmds = ['ffmpeg', '-i', video_path_unconverted, video_path_converted, '-hide_banner']
            subprocess.Popen(cmds)
        except:
            print("converting failed")
        
        time.sleep(2)


while True:
    for video in listdir(directory_path_unconverted):
        if isfile(join(directory_path_unconverted, video)):
            print(video)
            convert_video(video)
