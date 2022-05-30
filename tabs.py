import buttonEvent as B
import modules.dlconfig as config
import modules.userpass as credentials
import modules.servers as servers
import ctypes
from tkinter import *
from tkinter import ttk

class tabLists:

	def __init__(self, root, *args): #, nations, cities):

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

	def buttonEvent(self):

		self.selected = self.notebook.index('current')

		#print(self.selected)

		try:

			if self.selected == 0:
				selectionOne = str(self.lnations.curselection()).split("(")[1].strip(",)")
				nationCity = servers.nations()[int(selectionOne)]
				selection = servers.nationsPaths()[int(selectionOne)]

				print(nationCity); print(self.selection)

			if self.selected == 1:
				selectionTwo = str(self.lcities.curselection()).split("(")[1].strip(",)")
				nationCity = servers.cities()[int(selectionTwo)]
				selection = servers.citiesPaths()[int(selectionTwo)]

				print(nationCity); print(selection)
		except:
			
			print('Please Select Something')
	
		B.connectScript.connect(selection)

	def connectButton(self, text):

		connect = Button (text = text , command = tabLists(self).buttonEvent)
		connect.place(x=120,y=510)
