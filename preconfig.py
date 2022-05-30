
import modules.dlconfig as config
import modules.userpass as credentials
import modules.servers as servers

from tkinter import *
from tkinter import ttk
from random import randint

print("\x1bc")

setup = config.dlconfigs()

def configuration():

	print('Checking Directories...\n')

	setup.check_dirs(); setup.create_dirs()

	if setup.create_dirs()[2] == 1:

		print('Client found in: '+ setup.create_dirs()[1])

	setup.subprocess(); credentials.userPass()
	print("\x1bc")
