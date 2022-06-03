
import modules.dlconfig as config
import modules.userpass as credentials
import modules.servers as servers

from tkinter import *
from tkinter import ttk

def configuration():
	print('Checking Directories...\n')
	config.check_dirs(); config.create_dirs()
	
	if config.create_dirs()[2] == 1:

		print('Client found in: '+ config.create_dirs()[1])

	config.scripts(); credentials.userPass()
	
	print("\x1bc")
