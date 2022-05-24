from tkinter import *
from tkinter import ttk

import os
import subprocess
import shlex
import servers
import glob
import dlconfig as config
import random

setup = config.dlconfigs()

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

image = PhotoImage(file=('ipvanish-text-logo-white.png'))
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

def connectionScript():

	selection1 = lnations.curselection()		
	selection2 = str(lcities.curselection()).split("(")[1].strip(",)")
	city_selection = servers.cities()[int(selection2)]
		
	print(selection2)

	filelist=[]

	for i in glob.glob(str(setup.create_dirs()[0])+"*"+city_selection+"*"):
		filelist.append(i)

	filelist = sorted(filelist); length = len(filelist)
	random_server_dir = filelist[random.randint(0,length-1)]
	random_server = str(os.path.basename(random_server_dir)).strip(".ovpn")

	print('Connecting to Random '+ city_selection +' server' )

	subprocess.run( shlex.split ('nmcli connection import type openvpn file '+ random_server_dir), shell=False )
	subprocess.run( shlex.split ("sed -i 's:auth-user-pass:auth-user-pass " + setup.create_dirs()[0] + "credentials:g' " + random_server_dir ) , shell = False)

	subprocess.run( shlex.split ('nmcli connection up ' + random_server), shell=False)

#Connect Button
connect = Button ( ipvanish, text='Connect', command = connectionScript )
connect.place(x=125,y=520)


#Main Loop

ipvanish.mainloop()
