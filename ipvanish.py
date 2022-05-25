import os
import subprocess
import shlex
import modules.dlconfig as config
import modules.userpass as credentials
import modules.servers as servers
import glob

from tkinter import *
from tkinter import ttk
from random import randint


print("\x1bc")

setup = config.dlconfigs(); data = []

print('Checking Directories...\n')

setup.check_dirs()

setup.create_dirs()

if setup.create_dirs()[2] == 1:

	print('Client found in: '+ setup.create_dirs()[1])

setup.subprocess()

credentials.userPass()

#Main

ipvanish = Tk()
ipvanish.resizable(False,False)
ipvanish.geometry('340x600')
ipvanish.title('Ipvanish Client')

#Style

style = ttk.Style(ipvanish)
style.configure('TNotebook',height=50)

result = StringVar()

#Tabs

tab_parent = ttk.Notebook(ipvanish, style = 'TNotebook')

#Logo Image

image = PhotoImage(file=('assets/ipvanish-text-logo-white.png'))
canvas = Canvas(ipvanish, width=350,height=80)
canvas.create_image(5, 5, anchor=NW, image=image)
canvas.place(x=8,y=20)

#Tab One

tab_one = ttk.Frame(tab_parent, style = 'TNotebook')
tab_parent.add ( tab_one, text = 'Choose a Country:' )


#List in Tab One

nations = StringVar(value = servers.nations())
lnations = Listbox ( tab_one, listvariable = nations, height = 18)
lnations.grid ( column = 3, row = 3 , sticky = 'n')
lnations.place ( x=60, y=20)

#Tab Two

tab_two = ttk.Frame(tab_parent)
tab_parent.add ( tab_two, text = 'Choose a City:' )

#List in Tab Two

cities = StringVar ( value = servers.cities() )
lcities = Listbox ( tab_two, listvariable = cities, height = 18)
lcities.grid ( column = 3, row = 3 , sticky = 'nsew')
lcities.place ( x=60, y=20)

#Show Tabs

tab_parent.pack ( expand = True, fill = 'both', padx=30, pady=100)

#Loads of shit

def connectionScript():

	selection1 = lnations.curselection()		
	selection2 = str(lcities.curselection()).split("(")[1].strip(",)")
	city_selection = servers.citiesPath()[int(selection2)]

	filelist=[]

	for i in glob.glob(str(setup.create_dirs()[0])+"*"+city_selection+"*"):
		filelist.append(i)

	filelist = sorted(filelist); length = len(filelist)-1
	random_server_dir = filelist[randint(0,length)]
	random_server = str(os.path.basename(random_server_dir)).strip(".ovpn")

	
	print(random_server)
	print('Connecting to Random '+ city_selection +' server' )

	subprocess.run( shlex.split ('nmcli connection import type openvpn file '+ random_server_dir), shell=False )

	with open(setup.create_dirs()[0]+"credentials", 'r') as creds:

		for lines in creds:

			data.append(lines)
	creds.close()

	subprocess.run( shlex.split ("nmcli connection modify "+ random_server +" vpn.user-name "+ str(data[0]).strip("\n")),shell = False)
	
	subprocess.run(shlex.split ('nmcli connection modify '+ random_server +' vpn.secrets password='+ data[1]), shell = False)
	
	subprocess.run( shlex.split ('nmcli connection up ' + random_server), shell=False)

#Connect Button

connect = Button ( ipvanish, text='Connect', command = connectionScript )
connect.place(x=125,y=520)


#Main Loop

ipvanish.mainloop()
