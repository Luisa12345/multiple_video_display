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


print("screen -dmS screen0 sh -c 'omxplayer --display \"7\" --win \"0,0,640,1080\" /media/pi/toshiba/test/MOV_0133.mp4; exec bash'")


def get_available_files():
	directory_path = '/media/pi/toshiba/test'
	available_files = [f for f in listdir(directory_path) if isfile(join(directory_path, f))]
	
	return available_files

# play a video on given display and screen area
# def play_video(display=7, screen_area='0,0,640,480', video='MOV_0860.mp4'):
def play_video(screen, video):
	# omxplayer --display 7 --win 0,0,640,480 /media/pi/toshiba/test/MOV_0860.mp4^
	display = screen['display']
	screen_id = 'screen_' + str(screen['screen_id'])
	screen_area = screen['screen_area']

	bashCommand = 'screen -dmS ' + screen_id + ' sh -c ' + '\'' + 'omxplayer' +  ' --display ' + '"' + str(display) + '"' + ' --win ' + '"' + screen_area + '"' + ' /media/pi/toshiba/test/' + video + "; exec bash'"
	print(bashCommand)
	#exit()
	process = subprocess.Popen(bashCommand, stdout=subprocess.PIPE)
	output, error = process.communicate()	


def update_not_played_videos():
	not_played_videos = list(set(available_files) - set(played_videos))
	print(not_played_videos)


# returns screen areas: splitting the screen along the x axis

# TODO give names to screens! anbd displays!
def get_screens():
	if number_of_screens_per_display > 3:
		raise Exception('screen division for more than 3 screens not implemented yet')
		
	screens = []
	x_min = 0
	y_min = 0
	
	for display in displays:
		if number_of_screens_per_display == 1:
			screen_area =  [str(x) + ',' + str(y) + ',' + str(screen_resolution_x) + ',' + str(screen_resolution_y)]
			screens.append({'display': display, 'screen_id': 1, 'screen_area': screen_area})
		else:
			x_width = int(screen_resolution_x / number_of_screens_per_display)
			for screen_id in range(number_of_screens_per_display):
				x_max = x_min + x_width
				screen_area = (str(x_min) + ',' + str(y_min) + ',' + str(x_max) + ',' + str(screen_resolution_y))
				screens.append({'display': display, 'screen_id': screen_id, 'screen_area': screen_area}) 
				# shift x_min to next screen
				x_min = x_max
			
	return screens	


def play_init_videos():
	screens = get_screens()
	available_videos = get_available_files()
	for screen in screens:
		play_video(screen, available_videos[screen['screen_id']])

if __name__ == '__main__':
	# init display of all screens with start videos
	
    play_init_videos()
    

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


