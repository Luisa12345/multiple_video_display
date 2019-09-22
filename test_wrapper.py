
from omxplayer.player import OMXPlayer
from pathlib import Path
from time import sleep

VIDEO_PATH = Path("test.mp4")

player = OMXPlayer(VIDEO_PATH, args=['--display', str(7)])


sleep(5)

player.quit()
