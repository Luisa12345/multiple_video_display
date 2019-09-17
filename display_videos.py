import os
from os import listdir
from os.path import isfile, join
from omxplayer.player import OMXPlayer, BusFinder
from pathlib import Path
import time
import subprocess
from subprocess import run
import datetime

displays = [7] # HDMI 0 = 2, HDMI 1 = 7
number_of_screens_per_display = 2
screen_resolution_x = 1920
screen_resolution_y = 1080


def get_video_path():
    return os.getcwd() + '/videos/'

# gets all available files in video path
# TODO filter out non-videos files
def get_available_files():
    # directory_path = '/media/pi/toshiba/test'
    directory_path = get_video_path()
    available_files = [f for f in listdir(directory_path) if isfile(join(directory_path, f))]
    
    return available_files

def get_not_played_videos():
    not_played_videos = list(set(get_available_files()) - set(played_videos))
    print("**********************************************")
    print("not_played_videos")
    print(not_played_videos)
    print("**********************************************")
   
    if len(not_played_videos) == 0:
        print("no videos left to play") 
        #exit()
        
    
    return not_played_videos


# returns screen areas: splitting the screen along the x axis
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
                screens.append({'display': display, 'screen_id': screen_id, 'screen_area': screen_area, 'video_init_time': None, 'video': None, 'player': None}) 
                # shift x_min to next screen
                x_min = x_max
            
    return screens  

# iniits players for all screens with starting videos
def init_players():
    players = []
    players_and_screens = []
    screens = get_screens()
    available_videos = get_available_files()
    
    # TODO throw error if less files available than screens
    for screen in screens:
        video =  get_video_path() + available_videos[screen['screen_id']]
        player = play_with_library(screen, video)
        players.append(player)
        screen['video_init_time'] = time.time()
        screen['video'] = video
        screen['player'] = player
        played_videos.append(video)
        
    return screens
        
 
# starts a video on screen, using omxplayer_wrapper
def play_with_library(screen, video_path):
    #print(video_path)
    VIDEO_PATH = Path(video_path)
  
    # allocate a different dbus to each screen 
    dbus = "org.mpris.MediaPlayer2.omxplayer" + str(screen['screen_id']+1)
    player = OMXPlayer(VIDEO_PATH, args=['--display', str(7), '--win', str(screen['screen_area'])], dbus_name=dbus)          
    
    return player    

def initiate_new_player_if_necessary(screens):
    new_player_object = None
    replace_player= False
    
    for screen in screens:
        player = screen['player']
        
        try:
            #temporary solution to determine when player is about to reach the end of the video
            if player.position() > (player.duration() - 0.2):
                replace_player = True
                 
        except:
            print("could not communictate with player")
            
            # replace player only if video was started less than 5 seconds ago (video loading takes time) 
            if (time.time() - screen['video_init_time']) > 5:
                replace_player = True
            else:
                print("probably still loading")
                #print(player)
                #print(new_player_objects)
                replace_player = False

                #exit()
    
        if replace_player:
            # delete omxplayer instances in tmp folder
            subprocess.call("rm /tmp/omxplayer*", shell=True, stdout=subprocess.PIPE)
            
            # start new video
            new_player_object = play_with_library(screen, get_video_path() + get_not_played_videos()[0])
            played_videos.append(get_not_played_videos()[0])
            print("started new video")
            break
 
    # if there is a new video started, give it time to load 
    # and replace player object for screen with new player object
    if (new_player_object):
        time.sleep(2)
        screen['player'] = new_player_object
                
    return screens
    
if __name__ == '__main__':
    try:
        subprocess.call("rm /tmp/omxplayer*", shell=True, stdout=subprocess.PIPE)
    except:
        print("do nothing")
    
    # init display of all screens with start videos
    played_videos = []
    screens = init_players()
    new_player_object = None
    
    while True:
        # TODO return ojbect id of new player - store up to 3 newly initialized players in list -> if not responding to new player (because its loading) -> do nothing
        screens = initiate_new_player_if_necessary(screens)
