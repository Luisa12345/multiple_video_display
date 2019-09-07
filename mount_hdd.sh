#!bin/bash
sudo mkdir /media/pi/toshiba
sudo mount -t ntfs-3g -o uid=pi,gid=pi /dev/sdb1 /media/pi/toshiba
