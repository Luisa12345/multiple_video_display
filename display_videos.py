from os import listdir
from os.path import isfile, join
 
directory_path = '/media/pi/toshiba/test'
files = [f for f in listdir(directory_path) if isfile(join(directory_path, f))]
print(files)
