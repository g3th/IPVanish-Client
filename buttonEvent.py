import glob
import os
import shlex
import subprocess
import modules.dlconfig as config
import modules.userpass as credentials
import modules.servers as servers
import tabs

from tkinter import *
from random import randint

setup = config.dlconfigs(); data = []

class connectScript:

	def __init__(self, root, w, text):

		self.label = Label( root, width = w, text = text, borderwidth = 10)
		self.label.place(x=100,y=540)

	def connect(info, city_selection):
		print("\x1bc")
		filelist=[]

		for i in glob.glob(str(setup.create_dirs()[0])+"*"+city_selection+"*"):
			filelist.append(i)

		filelist = sorted(filelist); length = len(filelist)-1
		random_server_dir = filelist[randint(0,length)]
		random_server = str(os.path.basename(random_server_dir)).strip(".ovpn")

		print('Connecting to Random '+ info +' server\n' )

		
	
		subprocess.run( shlex.split ('nmcli connection import type openvpn file '+ random_server_dir), shell=False, stdout=subprocess.DEVNULL )

		with open(setup.create_dirs()[0]+"credentials", 'r') as creds:

			for lines in creds:

				data.append(lines)
		creds.close()

		subprocess.run(shlex.split ("nmcli connection modify "+ random_server +" vpn.user-name "+ str(data[0]).strip("\n")),shell = False, stdout=subprocess.DEVNULL)
	
		subprocess.run(shlex.split ('nmcli connection modify '+ random_server +' vpn.secrets password='+ data[1]), shell = False, stdout=subprocess.DEVNULL)
	
		subprocess.run( shlex.split ('nmcli connection up ' + random_server), shell=False, stdout=subprocess.DEVNULL)
	
		print("Connected to "+ info)

