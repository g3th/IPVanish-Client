import os
import requests
import concurrent.futures

from threading import Lock
from pathlib import Path
from bs4 import BeautifulSoup as soup
from tkinter import *
from tkinter import ttk

class configs_tab:
	
	def __init__(self, root, notebook):
		self.directory = str(Path(__file__).parents[1])+'/configs/'
		self.download_link = 'https://configs.ipvanish.com/configs/'
		self.file_number = 0
		self.lock = Lock()
		self.tab_four = ttk.Frame(root)
		notebook.add(self.tab_four, text = 'Configs')
		self.progress_bar = ttk.Progressbar(self.tab_four, orient = 'horizontal', mode = 'determinate', length = 100)
		self.progress_bar_title = Label(self.tab_four, text = 'Download Progress', font=('Arial',13))
		self.progress_bar_title.place(x=56,y=22)
		self.progress_bar.place(height=25,width=200,x=40,y=50)
		self.executor = concurrent.futures.ThreadPoolExecutor(20)
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
		links = fetch_links.find_all('span',{'class':'name'})
		for link in links:
			self.links_list.append(self.download_link+link.text.strip())
				
	def download_ovpn_files(self, download_link):
		download_request = requests.get(self.links_list[download_link]).content
		filename = str(self.links_list[download_link].split('/')[4])
		with open(self.directory + filename , 'wb') as zipped_config:
			zipped_config.write(download_request)			
		zipped_config.close()
		
	def fill_up_the_progressbar(self, future):
		self.lock.acquire()
		self.file_number +=1
		self.progress_bar['value'] += 1
		self.progress_bar_title.config(text = 'File {}/{}'.format(str(self.file_number),str(len(self.links_list))))
		self.lock.release()
				
	def threaded_downloads(self):
		self.fetch_and_parse_download_links()
		self.progress_bar.config(maximum = len(self.links_list))
		futures = [self.executor.submit(self.download_ovpn_files, link) for link in range(len(self.links_list))]
		for future in futures:
			future.add_done_callback(self.fill_up_the_progressbar)
			


				
