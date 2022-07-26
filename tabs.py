import glob
import os
import shlex
import subprocess
import modules.dlconfig as config
import modules.userpass as credentials
import modules.servers as servers

from tkinter import *
from tkinter import ttk
from random import randint

data = []


class tabLists:

	def __init__(self, root, *args):
		self.notebook = ttk.Notebook(root)

		self.tab_one = ttk.Frame(self.notebook)
		self.notebook.add(self.tab_one, text='Countries')

		self.tab_two = ttk.Frame(self.notebook)
		self.notebook.add(self.tab_two, text = 'Cities')
		
		nations = StringVar(value = servers.nations())
		self.lnations = Listbox (self.tab_one, listvariable = nations, height = 18)	
		self.lnations.grid ( column = 3, row = 3 , sticky = 'n')
		self.lnations.place (x=60, y=20)

		cities = StringVar(value = servers.cities())
		self.lcities = Listbox (self.tab_two, listvariable = cities, height = 18)
		self.lcities.grid ( column = 3, row = 3 , sticky = 'n')
		self.lcities.place ( x=60, y=20)
		self.notebook.pack(expand = True, fill = 'both', padx=30, pady=100)
		self.button_label = Label(root, text = 'Not Connected')
		self.connect_button = Button (root, text = 'Connect' , command = self.buttonEvent)
		
	def place_buttons(self):
	
		self.connect_button.place(x=133,y=515)
		self.button_label.place(x=124,y=555)

	def buttonEvent(self):		
		selected = self.notebook.index('current')
		try:

			if selected == 0:
				selectionOne = str(self.lnations.curselection()).split("(")[1].strip(",)")
				nationCity = servers.nations()[int(selectionOne)]
				selection = servers.nationsPaths()[int(selectionOne)]

			if selected == 1:
				selectionTwo = str(self.lcities.curselection()).split("(")[1].strip(",)")
				nationCity = servers.cities()[int(selectionTwo)]
				selection = servers.citiesPaths()[int(selectionTwo)]			
		except:			
			print('Please Select Something')
			
		self.connect(nationCity, selection)
		self.button_label['text']='Connected to '+ selection +' server\n'
		self.button_label.place(x=80,y=555)
	
	def connect(self,info, city_selection):
		filelist=[]
	
		for i in glob.glob(str(config.create_dirs()[0])+"*"+city_selection+"*"):
			filelist.append(i)
		filelist = sorted(filelist); length = len(filelist)-1
		random_server_dir = filelist[randint(0,length)]
		self.random_server = str(os.path.basename(random_server_dir)).strip(".ovpn")
		
		with open(config.create_dirs()[0]+"credentials", 'r') as creds:
			for lines in creds:
				data.append(lines)
		creds.close()
	
		import_connection = ['nmcli','connection','import','type','openvpn','file',random_server_dir]
		nmcli_connection_user_name = ['nmcli','connection','modify',self.random_server,'vpn.user-name',str(data[0]).strip("\n")]
		nmcli_connection_password = ['nmcli','connection','modify',self.random_server,'vpn.secrets','password='+data[1]]
		nmcli_connect = ['nmcli','connection','up',self.random_server]

		subprocess.run(import_connection, shell=False,stdout=subprocess.DEVNULL )
		subprocess.run(nmcli_connection_user_name, shell = False,stdout=subprocess.DEVNULL)
		subprocess.run(nmcli_connection_password, shell = False,stdout=subprocess.DEVNULL)
		subprocess.run(nmcli_connect, shell=False,stdout=subprocess.DEVNULL)		
		self.connect_button.config(text='Disconnect', command = self.disconnect)
		self.connect_button.place(x=125,y=515)
		
	def disconnect(self):
		delete_connection = ['nmcli','connection','delete','id',self.random_server]
		subprocess.run(delete_connection, shell=False, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
		self.connect_button.config(text='Connect', command = self.buttonEvent)
		self.button_label['text']='Not Connected'
		self.button_label.place(x=124,y=555)
