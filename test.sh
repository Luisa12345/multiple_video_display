#!bin/bash
screen -dmS screen0 sh -c 'omxplayer --display "7" --win "0,0,640,1080" /media/pi/toshiba/test/MOV_0133.mp4; exec bash'
screen -dmS screen0 sh -c 'omxplayer --display "7" --win "0,0,640,1080" /media/pi/toshiba/test/MOV_0133.mp4; exec bash'
screen -dmS screen1 sh -c 'omxplayer --display "7" --win "640,0,1280,1080" /media/pi/toshiba/test/MOV_0194.mp4; exec bash'
screen -dmS screen2 sh -c 'omxplayer --display "7" --win "1280,0,1920,1080" /media/pi/toshiba/test/MOV_0195.mp4; exec bash'

