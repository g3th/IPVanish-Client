import os
import requests
import subprocess
import shlex
from pathlib import Path

page = 'https://www.ipvanish.com/software/configs/configs.zip'
#find = shlex.split ('find /home -type d -name IPVanish-Client')

#print("\x1bc")

		
def check_dirs():

	
	directory = str(Path(__file__).parents[1])
	return directory

def create_dirs():
	flag=0
	dirs = check_dirs()
	configs = dirs + "/configs/"

	if 'IPVanish-Client' in dirs:

		flag=1

	return configs, dirs, flag

def scripts():

	cdir = create_dirs()[0]
	dir_ = create_dirs()[1]


	if os.path.exists(cdir) == False :

		print('Created "configs" directory \n')

		os.mkdir (cdir)
	
	if len(os.listdir(cdir)) < 1:

		print("Downloading/Unzipping Config files")

		subprocess.run(shlex.split('wget "'+page +'" -P ' + cdir), shell=False, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)

		subprocess.run(shlex.split('unzip '+ cdir +'configs.zip'+' -d '+ cdir), shell=False, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)

		subprocess.run(shlex.split('rm '+ cdir +'configs.zip'))
	else:
		print("\nConfiguration files already exist\n")
