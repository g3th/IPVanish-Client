import os
import requests
import concurrent.futures
from pathlib import Path
from bs4 import BeautifulSoup as soup
from tkinter import *
from tkinter import ttk

class configs_tab:
	
	def __init__(self, root, notebook):
		self.directory = str(Path(__file__).parents[1])+'/configs/'
		self.download_link = 'https://configs.ipvanish.com/configs/'
		self.tab_four = ttk.Frame(root)
		notebook.add(self.tab_four, text = 'Configs')
		self.progressbar = ttk.Progressbar(self.tab_four, orient = 'horizontal', mode = 'determinate', length = 150)
		self.progressbar.place(height=25,width=200,x=40,y=40)
		self.check_if_configs_exist()
		
	def check_if_configs_exist(self):
		while True:
			try:
				if len(os.listdir(self.directory)) > 1:
					label_test = Label(self.tab_four, font=('Arial',13),text='Config Files Already Exist')
					label_test.place(x=33,y=78)
					break
				else:
					self.configs_button = Button(self.tab_four, text='Download Open-VPN Config Files',command=self.threaded_downloads)
					self.configs_button.place(x=20,y=90)
					break
			except OSError:
				os.mkdir (self.directory)
				pass
						
	def fetch_and_parse_download_links(self):
	
		self.links_list=[]
		request = requests.get(self.download_link)
		fetch_links = soup(request.content,'html.parser')
		links = fetch_links.find_all('a',href=True)
		for link in links:
			self.progressbar['value']+=1
			self.links_list.append(self.download_link+link.text.strip())
			self.tab_four.update()
				
	def download_ovpn_files(self, download_link):
		download_request = requests.get(self.links_list[download_link]).content
		filename = str(self.links_list[download_link].split('/')[4])
		with open(self.directory + filename , 'wb') as zipped_config:
			zipped_config.write(download_request)
	
	def progress_bar_increment(self):
		self.progressbar['value'] +=1
				
	def threaded_downloads(self):
		self.fetch_and_parse_download_links()
		list_of_futures = []
		self.progressbar['value'] = 0
		with concurrent.futures.ThreadPoolExecutor(100) as executor:
			for link in range(len(self.links_list)):
				try:
					list_of_futures = [executor.submit(self.download_ovpn_files, link) for i in range(len(self.links_list))]
					for future in list_of_futures:
						future.add_done_callback(self.progress_bar_increment)
				except OSError:
					continue
				
				
