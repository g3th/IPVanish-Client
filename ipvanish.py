import os
import requests
import subprocess
import shlex

print('\x1bc')

ctr=0 ; progress='#';files=[]; path='/home'

page='https://www.ipvanish.com/software/configs/configs.zip'

print("Checking Directories")

directory_=subprocess.check_output(shlex.split ('find /home -type d -name "IPVanish-Client"'), shell=False)

directory = str(directory_).strip("b'").strip("\\n")
configs=directory+"/configs"

if 'IPVanish-Client' in directory:
	
	print('Client found in: ' + directory)


if 'configs' not in os.listdir(directory):
	
	print('Created "configs" directory \n')

	os.mkdir (directory + "/configs")

print("Downloading/Unzipping Config files")

subprocess.run(shlex.split('wget "'+page+'" -P '+directory+'/configs/'), shell=False, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)

subprocess.run(shlex.split('unzip '+configs+'/configs.zip'+' -d '+configs), shell=False, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)

subprocess.run(shlex.split('rm '+configs+'/configs.zip'))
