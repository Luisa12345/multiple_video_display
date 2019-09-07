from os import listdir
from os.path import isfile, join
from omxplayer.player import OMXPlayer
from pathlib import Path
import time
import subprocess

displays = [7] # HDMI 0 = 2, HDMI 1 = 7
number_of_screens_per_display = 3
screen_resolution_x = 1920
screen_resolution_y = 1080
 

# play a video on given display and screen area
def play_video(display=7, screen_area='0,0,640,480', video='MOV_0860.mp4'):
	# omxplayer --display 7 --win 0,0,640,480 /media/pi/toshiba/test/MOV_0860.mp4^
	bashCommand = 'omxplayer' +  '--display ' + str(display) + '--win ' + screen_area + '/media/pi/toshiba/test/' + video
	process = subprocess.Popen(bashCommand, stdout=subprocess.PIPE)
	output, error = process.communicate()	


def update_not_played_videos():
	not_played_videos = list(set(available_files) - set(played_videos))
	print(not_played_videos)


# returns screen areas: splitting the screen along the x axis
def get_screen_areas():
	if number_of_screens_per_display > 3:
		raise Exception('screen division for more than 3 screens not implemented yet')
	
	
	if number_of_screens_per_display == 1:
		return [str(0) + ',' + str(0) + ',' + str(screen_resolution_x) + ',' + str(screen_resolution_y)]
			
	screens = []
	x = 0
	y = 0
	x_width = int(screen_resolution_x / number_of_screens_per_display)
	for screen in range(number_of_screens_per_display):
		x_max = x + x_width
		screens.append(str(x) + ',' + str(y) + ',' + str(x_max) + ',' + str(screen_resolution_y))
		x = x_max
	
	return screens	
	

print(get_screen_areas())
#play_video()


# only worked once - why??
def play_with_library():
	VIDEO_PATH = Path("/media/pi/toshiba/test/MOV_0860.mp4", args=["--display 7"])

	player = OMXPlayer(VIDEO_PATH, dbus_name='org.mpris.MediaPlayer2.omxplayer2')
	print(player)

	player.play()
	player.show_video()


	print(player.is_playing())
	print(player.playback_status())

	time.sleep(15)

	player.quit()


	#print(files)


