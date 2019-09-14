#!bin/bash
sudo umount /media/pi/toshiba1
sudo umount /media/pi/toshiba
sudo mkdir /media/pi/toshiba
sudo mount -t ntfs-3g -o uid=pi,gid=pi /dev/sda1 /media/pi/toshiba
sudo mount -t ntfs-3g -o uid=pi,gid=pi /dev/sdb1 /media/pi/toshiba
