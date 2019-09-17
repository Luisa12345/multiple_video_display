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
                screens.append({'display': display, 'screen_id': screen_id, 'screen_area': screen_area, 'video_init_time': None, 'video': None, 'player': None}) 
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
        #if screen['screen_id'] == 1:
         #   continue
        video =  get_video_path() + available_videos[screen['screen_id']]
        player = play_with_library(screen, video)
        players.append(player)
        screen['video_init_time'] = datetime.datetime.now()
        screen['video'] = datetime.datetime.now()
        screen['player'] = player
        players_and_screens.append({'screen': screen, 'player': player})
        played_videos.append(video)
        
    return players, players_and_screens
        
    

# only worked once - why??
def play_with_library(screen, video_path):
    #print(video_path)
    VIDEO_PATH = Path(video_path)
    
    print(VIDEO_PATH)
  
    # try different dbus
    #  bus = ["org.mpris.MediaPlayer2.omxplayer2" ,"org.mpris.MediaPlayer2.omxplayer3",]
    # OMXPlayer(path + vid, args=['--layer', str(1), '--display', str(7)], dbus_name=bus[1])
    dbus = "org.mpris.MediaPlayer2.omxplayer" + str(screen['screen_id']+1)
    player = OMXPlayer(VIDEO_PATH, args=['--display', str(7), '--win', str(screen['screen_area'])], dbus_name=dbus)
            
    #player.hide_video()
    
    return player    

# TODO use only screens    
def initiate_new_player_if_necessary(player_objects, players_and_screens, new_player_objects):
    new_player_object = None
    replace_player= False
    
    
    # TODO add video name and video_init_time to screen
    # if video init time is more than 5sec ago replace
    # delete video from played list
    
    for player_id ,player_and_screen in enumerate(players_and_screens):
        print(player_and_screen)
        exit()
        screen = player_and_screen['screen']
        player = screen['player']
            #player = player_and_screen['player']
            #screen = player_and_screen['screen']
            #player is close to the end of its movie
        try:
         if player_object.position() > (player_object.duration() - 0.2): #temporary solution to determine when player is about to reach the end of the video
            #replace_player = True
            player_object.quit()

        except:
            print("could not communictate with player")
            
            # TODO: check screen instead!! is already loading for screen???
            if screen['video_init_time'] > datetime.datetime.now() - 5:
                replace_player = True
            else:
                
                print("probably still loading")
                print(player_object)
                print(new_player_objects)
                replace_player = False

                #exit()
    
        if replace_player:
            subprocess.call("rm /tmp/omxplayer*", shell=True, stdout=subprocess.PIPE)
       
            #get screen for player!
            for player_and_screen in players_and_screens:
                if player_object == player_and_screen['player']:
                    print("replacing player instance", player_and_screen['screen']['screen_area'])
                    #player_and_screen['player'] = None
                    # overwrite player object with new player
                    print("current player", player_object)
                    new_player_object = play_with_library(player_and_screen['screen'], get_video_path() + get_not_played_videos()[0])
                    print("started new video")
                    player_id_renewed = player_id
                    break
 
            # update player_objects list and players_and_screens with new player
    if (new_player_object):
        time.sleep(2)
        print("updated player", new_player_object)
        players_and_screens[player_id_renewed]['screen']['player'] = new_player_object
        player_objects[player_id_renewed] = new_player_object
        
        #print("player_objects", player_objects)
        #exit()
        print(players_and_screens)
                
    return player_objects, players_and_screens, new_player_object
    
if __name__ == '__main__':
    try:
        subprocess.call("rm /tmp/omxplayer*", shell=True, stdout=subprocess.PIPE)
    except:
        print("do nothing")
    
    # init display of all screens with start videos
    played_videos = []
    player_objects, players_and_screens = init_players()
    #print(len(player_objects), players_and_screens)
    new_player_object = None
    new_player_objects = []
    
    while True:
        print(len(player_objects))
        if new_player_object is not None:
            if len(new_player_objects) <= 2:
                new_player_objects.append(new_player_object)
            else:
                print("more than 2 new players")
                print(len(new_player_objects))
                new_player_objects.pop()
                new_player_objects.append(new_player_object)

            
        
        # TODO return ojbect id of new player - store up to 3 newly initialized players in list -> if not responding to new player (because its loading) -> do nothing
        player_objects, players_and_screens, new_player_object = initiate_new_player_if_necessary(player_objects, players_and_screens, new_player_objects)
        
        
        
    
                            
                        
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
  
