import os
import requests
import concurrent.futures

from threading import Lock
from bs4 import BeautifulSoup as soup
from pathlib import Path
from tkinter import *
from tkinter import ttk

class GUI:

	def __init__(self):
				
		self.root = Tk()
		self.root.title('Progress Bar Test')
		self.root.geometry('300x150')
		self.root.resizable(False,False)
		self.file_number = 0
		self.lock = Lock() # Mutual Exclusion Lock in Python
		self.executor = concurrent.futures.ThreadPoolExecutor(20)
		self.download_link='https://configs.ipvanish.com/configs/'
		self.directory = str(Path(__file__).parent)+'/config/'
		self.button_choices= Button(self.root,text='Download Configs', command=self.threaded_download)
		self.button_choices.place(x=80,y=105)
		
	def draw_the_Progress_Bar(self):
	
		self.progress_bar = ttk.Progressbar(self.root, orient = 'horizontal', mode='determinate',length=100)
		self.progress_bar.place(height=30,width=200,x=50,y=60)
		self.progress_bar_title = Label(text = 'Download Progress', font=('Arial',15))
		self.progress_bar_title.place(x=60,y=28)
		
	def fetch_and_parse_download_links(self):
	
		os.makedirs(self.directory,exist_ok=True)
		self.links_list=[]
		request = requests.get(self.download_link)
		fetch_links = soup(request.content,'html.parser')
		links = fetch_links.find_all('span',{'class':'name'})
		for link in links:
			self.links_list.append(self.download_link+link.text.strip())

	def fill_up_the_progress_bar(self, future):
	
		self.lock.acquire() # This stops a race condition
		self.file_number +=1
		self.progress_bar['value']+=1
		self.progress_bar_title.config(text = 'Downloading File {}'.format(str(self.file_number)))
		self.lock.release()
				
	def download_ovpn_configuration_files(self, download_link):
	
		download_request = requests.get(self.links_list[download_link]).content
		filename = str(self.links_list[download_link].split('/')[4])
		with open(self.directory + filename , 'wb') as zipped_config:
			zipped_config.write(download_request)
		
	def threaded_download(self):
	
		self.fetch_and_parse_download_links()
		self.progress_bar.config(maximum = len(self.links_list))
		self.progress_bar_title.place(x=50,y=28)
		futures = [self.executor.submit(self.download_ovpn_configuration_files, link) for link in range(len(self.links_list))]
		for future in futures:
			future.add_done_callback(self.fill_up_the_progress_bar)
	
	def Window_Loop(self):
		
		self.root.mainloop()

if __name__ == ('__main__'):

	test = GUI()
	test.draw_the_Progress_Bar()
	test.Window_Loop()
