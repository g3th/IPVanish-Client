import os
import requests
import subprocess
import shlex

class dlconfigs():
	
	def __init__(self):
		
		self.flag =  0
		self.path = 'home'
		self.page = 'https://www.ipvanish.com/software/configs/configs.zip'
		self.find = shlex.split ('find /home -type d -name "IPVanish-Client"')

		
	def check_dirs(self):

		directory_=subprocess.check_output(self.find, shell=False)

		directory = str(directory_).strip("b'").strip("\\n")

		return directory

	def create_dirs(self):

		dirs = dlconfigs.check_dirs(self)
		configs = dirs + "/configs/"
		
		if 'IPVanish-Client' in dirs:

			flag=1

		return configs, dirs, flag

	def subprocess(self):

		cdir = dlconfigs.create_dirs(self)[0]
		dir_ = dlconfigs.create_dirs(self)[1]
	

		if 'configs' not in os.listdir(dir_):
	
			print('Created "configs" directory \n')

			os.mkdir (cdir)
			
		if len(os.listdir(cdir)) < 1:

			print("Downloading/Unzipping Config files")

			subprocess.run(shlex.split('wget "'+self.page +'" -P ' + cdir), shell=False, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)

			subprocess.run(shlex.split('unzip '+ cdir +'configs.zip'+' -d '+ cdir), shell=False, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)

			subprocess.run(shlex.split('rm '+ cdir +'configs.zip'))
		else:
			print("\nConfiguration files already exist\n")

