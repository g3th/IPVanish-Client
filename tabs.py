import glob
import os
import subprocess
import modules.dlconfig as config
import modules.userpass as credentials
import modules.servers as servers
from pathlib import Path
from tkinter import *
from tkinter import ttk
from random import randint

class tabLists:

	def __init__(self, root, *args):
	
		self.file_path = str(Path(__file__).parent)
		self.credentials = []
		
		self.notebook = ttk.Notebook(root)

		self.tab_one = ttk.Frame(self.notebook)
		self.notebook.add(self.tab_one, text='Countries')

		self.tab_two = ttk.Frame(self.notebook)
		self.notebook.add(self.tab_two, text = 'Cities')
		
		self.tab_three = ttk.Frame(self.notebook)
		self.notebook.add(self.tab_three, text = 'Credentials')
		
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
		
		self.user_name = Entry(self.tab_three)
		self.password = Entry(self.tab_three,show='*')
		self.store_credentials_button = Button(self.tab_three, text = 'Save Credentials', command =self.store_credentials)
		self.store_credentials_button.place(x=66, y=151)
		self.connect_button.place(x=133,y=515)
		self.button_label.place(x=124,y=555)
		
		if 'credentials' in os.listdir(self.file_path):
			with open('credentials','r') as existing_credentials:
				for credential in existing_credentials.readlines():
					self.credentials.append(credential)			
			self.display_stored_credentials(self.credentials[0],self.credentials[1])
		else:			
			self.entry_boxes()
			
	def entry_boxes(self):		
		self.user_name_label = Label(self.tab_three, text = 'User Name: ')
		self.password_label = Label(self.tab_three, text = 'Password: ')
		self.user_name_label.place(x=55,y=35)
		self.user_name.place(x=55,y=60)	
		self.password_label.place(x=55,y=88)			
		self.password.place(x=55,y=115)
		
		
	def store_credentials(self):
		self.credentials = [self.user_name.get(), self.password.get()]
		if self.credentials == ['','']:
			self.no_credentials()
		else:
			for credential in self.credentials:
				with open('credentials', 'a') as write_creds:
					write_creds.write(credential + "\n")
				write_creds.close()
			self.display_stored_credentials(self.credentials[0],self.credentials[1])
			
	def display_stored_credentials(self,user,password):
	
		self.store_credentials_button.config(text = 'Clear Credentials', command =self.delete_credentials)
		self.displayed_user_name = Label(self.tab_three, text = user)
		self.displayed_user_name.place(x=55,y=58)
		self.displayed_password = Label(self.tab_three, text = '*'*(len(password)))
		self.displayed_password.place(x=55,y=112)
		self.password.destroy()
		self.user_name.destroy()
		
	def delete_credentials(self):
		
		os.remove('credentials')
		self.store_credentials_button.config(text = 'Save Credentials', command =self.store_credentials)
		self.displayed_user_name.destroy()
		self.displayed_password.destroy()
		self.entry_boxes()
	
	def no_selection(self):
		
		nothing_selected_error = Toplevel(self.notebook)
		nothing_selected_error.geometry("160x70")
		nothing_selected_error.resizable(False,False)
		nothing_selected_error.title("Error")
		Label(nothing_selected_error, font=("Arial", 13),text='Please Select \na Server').place(x=14,y=8)
	
	def no_credentials(self):
		no_credentials_error = Toplevel(self.notebook)
		no_credentials_error.geometry("160x70")
		no_credentials_error.resizable(False,False)
		no_credentials_error.title("Error")
		Label(no_credentials_error, font=("Arial", 13),text='Please Enter \nUser Credentials').place(x=14,y=8)

	def buttonEvent(self):
		if self.credentials == []:
			self.no_credentials()
		else:			
			try:
				selected = self.notebook.index('current')
				if selected == 0:
					selectionOne = str(self.lnations.curselection()).split("(")[1].strip(",)")
					nationCity = servers.nations()[int(selectionOne)]
					selection = servers.nationsPaths()[int(selectionOne)]

				if selected == 1:
					selectionTwo = str(self.lcities.curselection()).split("(")[1].strip(",)")
					nationCity = servers.cities()[int(selectionTwo)]
					selection = servers.citiesPaths()[int(selectionTwo)]
				self.connect(nationCity, selection)
				self.button_label['text']='Connected to '+ selection +' server\n'
				self.button_label.place(x=80,y=555)
				
			except:
				self.no_selection()
			
	
	def connect(self,info, city_selection):
		data = []
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
