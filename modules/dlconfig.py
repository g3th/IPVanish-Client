import os
import requests
import concurrent.futures
import shutil

from threading import Lock
from pathlib import Path
from bs4 import BeautifulSoup as Soup
from tkinter import *
from tkinter import ttk


class ConfigsTab:

    def __init__(self, root, notebook):
        self.configs_download_button = None
        self.delete_and_download_again_button = None
        self.progress_bar_title = None
        self.progress_bar = None
        self.links_list = None
        self.directory = str(Path(__file__).parents[1]) + '/configs/'
        self.download_link = 'https://configs.ipvanish.com/configs/'
        self.file_number = 0
        self.lock = Lock()  # Python Mutual Exclusive Lock (GIL)
        self.tab_four = ttk.Frame(root)
        notebook.add(self.tab_four, text='Configs')
        self.executor = concurrent.futures.ThreadPoolExecutor(20)
        self.check_if_configs_exist()

    def draw_the_progressbar(self):

        self.progress_bar = ttk.Progressbar(self.tab_four, orient='horizontal', mode='determinate', length=100)
        self.progress_bar_title = Label(self.tab_four, text='Download Progress', font=('Arial', 13))
        self.progress_bar_title.place(x=56, y=22)
        self.progress_bar.place(height=25, width=200, x=40, y=50)

    def check_if_configs_exist(self):
        self.draw_the_progressbar()
        while True:
            try:
                if len(os.listdir(self.directory)) > 1:
                    self.progress_bar_title.config(font=('Arial', 13), text='Config Files Found!')
                    self.delete_and_download_again_button = Button(self.tab_four, text='Delete and Re-Download Configs',
                                                                   command=self.delete_and_download_again)
                    self.delete_and_download_again_button.place(x=20, y=90)
                    self.progress_bar.destroy()
                    break
                else:
                    self.configs_download_button = Button(self.tab_four, text='Download Open-VPN Config Files',
                                                          command=self.threaded_downloads)
                    self.configs_download_button.place(x=20, y=90)
                    break
            except OSError:
                os.mkdir(self.directory)
                pass

    def delete_and_download_again(self):
        self.draw_the_progressbar()
        shutil.rmtree(self.directory)
        self.delete_and_download_again_button.destroy()
        self.threaded_downloads()

    def fetch_and_parse_download_links(self):
        self.links_list = []
        request = requests.get(self.download_link)
        fetch_links = Soup(request.content, 'html.parser')
        links = fetch_links.find_all('span', {'class': 'name'})
        for link in links:
            self.links_list.append(self.download_link + link.text.strip())

    def download_ovpn_files(self, download_link):
        download_request = requests.get(self.links_list[download_link]).content
        filename = str(self.links_list[download_link].split('/')[4])
        with open(self.directory + filename, 'wb') as zipped_config:
            zipped_config.write(download_request)
        zipped_config.close()

    def fill_up_the_progressbar(self, future):
        self.lock.acquire()  # the Mutex Prevents a Race condition
        self.file_number += 1
        self.progress_bar['value'] += 1
        self.progress_bar_title.config(text='File {}/{}'.format(str(self.file_number), str(len(self.links_list))))
        self.lock.release()  # Release the Kraken

    def threaded_downloads(self):
        self.fetch_and_parse_download_links()
        self.configs_download_button.destroy()
        self.progress_bar.config(maximum=len(self.links_list))
        futures = [self.executor.submit(self.download_ovpn_files, link) for link in range(len(self.links_list))]
        for future in futures:
            future.add_done_callback(self.fill_up_the_progressbar)
