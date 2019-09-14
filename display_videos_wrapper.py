import os
from os import listdir
from os.path import isfile, join
from omxplayer.player import OMXPlayer, BusFinder
from pathlib import Path
import time
import subprocess
from subprocess import run

displays = [7] # HDMI 0 = 2, HDMI 1 = 7
number_of_screens_per_display = 3
screen_resolution_x = 1920
screen_resolution_y = 1080



#print("screen -dmS screen0 sh -c 'omxplayer --display \"7\" --win \"0,0,640,1080\" /media/pi/toshiba/test/MOV_0133.mp4; exec bash'")

def get_video_path():
    return os.getcwd() + '/videos/'

def get_available_files():
    # directory_path = '/media/pi/toshiba/test'
    directory_path = get_video_path()
    available_files = [f for f in listdir(directory_path) if isfile(join(directory_path, f))]
    
    return available_files

def get_not_played_videos():
    not_played_videos = list(set(get_available_files()) - set(played_videos))
    print(not_played_videos)
    
    return not_played_videos


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


def init_players():
    players = []
    players_and_screens = []
    screens = get_screens()
    available_videos = get_available_files()
    
    # TODO throw error if less files available than screens
    
    for screen in screens:
        if screen['screen_id'] == 1:
            continue
        video = available_videos[screen['screen_id']]
        player = play_with_library(screen, get_video_path()  + video)
        players.append(player)
        players_and_screens.append({'screen': screen, 'player': player})
        played_videos.append(video)
        
    return players, players_and_screens
        
    

# only worked once - why??
def play_with_library(screen, video_path):
    #print(video_path)
    VIDEO_PATH = Path(video_path)
  
    # try different dbus
    #  bus = ["org.mpris.MediaPlayer2.omxplayer2" ,"org.mpris.MediaPlayer2.omxplayer3",]
    # OMXPlayer(path + vid, args=['--layer', str(1), '--display', str(7)], dbus_name=bus[1])
    player = OMXPlayer(VIDEO_PATH, args=['--display', str(7), '--win', str(screen['screen_area'])])#, dbus_name="org.mpris.MediaPlayer2.omxplayer3")
            
    #player.hide_video()
    
    return player       
    
    
if __name__ == '__main__':
    # init display of all screens with start videos
    played_videos = []
    player_objects, players_and_screens = init_players()
    print(len(player_objects), players_and_screens)
 
    while True:
        print(len(player_objects))
        #not_played_videos = get_not_played_videos()
        #not_played = []
        
        for player_object in player_objects:
            #player = player_and_screen['player']
            #screen = player_and_screen['screen']
            #player is close to the end of its movie
            if player_object.position() > (player_object.duration() - 0.5) : #temporary solution to determine when player is about to reach the end of the video
                #get screen for player!
                for player_and_screen in players_and_screens:
                    if player_object == player_and_screen['player']:
                        print("deleting player instance")
                        #player_and_screen['player'] = None
                        print("started new video")
                        player_object.quit()
                        # overwrite player object with new player
                        player_object = play_with_library(player_and_screen['screen'], get_not_played_videos()[0])
                        player_and_screen['player'] = player_object
    
                            
                        
                #del player['player']
            
            #player.quit()
        
            #print(player.is_playing())
            
            # ? connect screen and player in dict? {screeen: screen_id, player: player}  -> except -> play for screen
            
            # todo , try quit callback where player is added to "not playing anymore " list?
            
            # TODO if this doesnt work - because it is not aksing the right player - try differnt dbus first , then go via ps aux or something
            #pi@raspberrypi:~/multiple_video_display $ ps aux | grep omx
            #pi        3102  0.1  0.0   7676  2928 ?        Ss   16:38   0:00 /bin/bash /usr/bin/omxplayer --display 7 --win 0,0,640,1080 /home/pi/multiple_video_display/videos/test_2.mp4

            # 
          #  if not player.is_playing():
          #      if not_played_videos not []:
                    
          #          player.load(not_played_videos[0])
          #          player.play()
          #          player.show_video()
  
