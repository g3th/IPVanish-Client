import os
import requests
import subprocess
import shlex
from pathlib import Path
from tkinter import *
from tkinter import ttk



class configs_tab:
	
	def __init__(self, root, notebook):
		self.directory = str(Path(__file__).parents[1])+'/configs'
		self.download_link = 'https://www.ipvanish.com/software/configs/configs.zip'
		self.tab_four = ttk.Frame(root)
		notebook.add(self.tab_four, text = 'Configs')
		self.progressbar = ttk.Progressbar(self.tab_four, orient = 'horizontal', mode = 'determinate', length = 150)
		self.progressbar.place(height=25,width=200,x=40,y=40)
		self.check_if_configs_exist()
		
	def check_if_configs_exist(self):
		if len(os.listdir(self.directory)) > 1:
			label_test = Label(self.tab_four, font=('Arial',15),text='Config Files Already Exist')
			label_test.place(x=20,y=85)
		else:
			self.configs_button = Button(self.tab_four, text='Download Open-VPN Config Files',command=self.download_configs)
			self.configs_button.place(x=20,y=180)
			
	def download_configs(self):
		return 0
		
		
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
