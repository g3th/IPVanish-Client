import threading
import time
import modules.dlconfig as config
from modules.servers import nations as n
from modules.servers import cities as c
from pathlib import Path
from tkinter import *
from tkinter import ttk
import os
from establish_connection import EstablishConnection
from parse_ovpn_configuration_file import ParseConfigurationFile


class TabsLists:

    def __init__(self, root):
        self.pid = None
        self.connect = None
        self.selection = None
        self.process_pid = None
        self.openvpn_command = None
        self.ipvanish_dns = ['198.18.0.1', '198.18.0.2']
        self.default_gateway = '192.168.0.1'
        self.loopback = '192.168.0.1'
        self.current_interface = []
        self.user_name = None
        self.password = None
        self.sudo_password = None # Set your password here if you don't want to enter it every time
        self.user_name_label = None
        self.password_label = None
        self.displayed_user_name = None
        self.displayed_password = None
        self.random_server = None
        self.configuration_files_path = str(Path(__file__).parent) + '/configs'
        self.credentials = []
        self.notebook = ttk.Notebook(root)
        self.tab_one = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_one, text='Countries')
        self.tab_two = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_two, text='Cities')
        self.tab_three = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_three, text='Credentials')
        config.ConfigsTab(root, self.notebook)
        nations = StringVar(value=n)
        self.list_of_nations = Listbox(self.tab_one, listvariable=nations, height=18)
        self.list_of_nations.grid(column=3, row=3, sticky='n')
        self.list_of_nations.place(x=60, y=20)
        cities = StringVar(value=c)
        self.list_of_cities = Listbox(self.tab_two, listvariable=cities, height=18)
        self.list_of_cities.grid(column=3, row=3, sticky='n')
        self.list_of_cities.place(x=60, y=20)
        self.notebook.pack(expand=True, fill='both', padx=30, pady=100)
        self.button_label = Label(root, text='Not Connected')
        self.connect_button = Button(root, text='Connect', command=self.connect_button_event_as_thread)
        self.store_credentials_button = Button(self.tab_three, text='Save Credentials', command=self.store_credentials)
        self.store_sudo_credentials_button = Button(self.tab_three, text='Save Sudo Password',
                                                    command=self.store_sudo_password)
        self.store_sudo_credentials_button.place(x=60, y=250)
        self.store_credentials_button.place(x=66, y=151)
        self.connect_button.place(x=133, y=515)
        self.button_label.place(x=121, y=555)

        if 'credentials' in os.listdir(self.configuration_files_path):
            with open(self.configuration_files_path + '/credentials', 'r') as existing_credentials:
                for credential in existing_credentials.readlines():
                    self.credentials.append(credential)
            self.entry_boxes()
            self.display_stored_credentials(self.credentials[0], self.credentials[1])
        else:
            self.entry_boxes()

    def entry_boxes(self):
        self.user_name = Entry(self.tab_three)
        self.user_name.place(x=55, y=58)
        self.user_name_label = Label(self.tab_three, text='User Name: ')
        self.user_name_label.place(x=55, y=35)
        self.password = Entry(self.tab_three, show='*')
        self.password.place(x=55, y=118)
        self.password_label = Label(self.tab_three, text='Password: ')
        self.password_label.place(x=55, y=96)
        self.sudo_password_box = Entry(self.tab_three, show="*")
        self.sudo_password_box.place(x=55, y=220)
        self.sudo_password_box_label = Label(self.tab_three, text='Sudo Password: ')
        self.sudo_password_box_label.place(x=55, y=190)

    def store_credentials(self):
        self.credentials = [self.user_name.get(), self.password.get()]
        if self.credentials == ['', '']:
            self.error("Please Enter\nAccount Credentials", "200","200")
        else:
            for credential in self.credentials:
                with open(self.configuration_files_path + "/credentials", 'a') as write_creds:
                    write_creds.write(credential + "\n")
                write_creds.close()
            self.display_stored_credentials(self.credentials[0], self.credentials[1])

    def store_sudo_password(self):
        self.sudo_password = self.sudo_password_box.get()
        if self.sudo_password == "":
            self.error("Please Enter\nSudo Password", "200","200")
        else:
            self.sudo_password_box.destroy()
            display_sudo_password = Label(self.tab_three, text="*" * len(self.sudo_password))
            display_sudo_password.place(x=55, y=220)

    def error(self, message, x, y):
        error = Toplevel(self.notebook)
        error.geometry("{}x{}".format(x, y))
        error.resizable(False, False)
        error.title("Error")
        Label(error, font=("Arial", 13), text= message).place(x=14, y=8)

    def display_stored_credentials(self, user, password):
        self.store_credentials_button.config(text='Clear Credentials', command=self.delete_credentials)
        self.displayed_user_name = Label(self.tab_three, text=user)
        self.displayed_user_name.place(x=55, y=58)
        self.displayed_password = Label(self.tab_three, text='*' * (len(password)))
        self.displayed_password.place(x=55, y=118)
        self.password.destroy()
        self.user_name.destroy()

    def delete_credentials(self):
        os.remove(self.configuration_files_path + '/credentials')
        self.entry_boxes()
        self.store_credentials_button.config(text='Save Credentials', command=self.store_credentials)
        self.displayed_user_name.destroy()
        self.displayed_password.destroy()

    def buttonEvent(self):
        selection = None
        if not self.credentials:
            self.error("Please Enter\nAccount Credentials", "180","60")
        else:
            # try:
            selected = self.notebook.index('current')
            match selected:
                case 0:
                    selection_index = self.list_of_nations.curselection()
                    self.selection = self.list_of_nations.get(selection_index)
                case 1:
                    selection_index = self.list_of_nations.curselection()
                    self.selection = self.list_of_nations.get(selection_index)
            if self.sudo_password is None:
                self.error("Please Enter\nSudo Password", "150","60")
            else:
                self.connect = EstablishConnection(self.sudo_password)
                self.create_connection()
                self.button_label['text'] = 'Connected to ' + self.selection + ' server\n'
                self.button_label.place(x=80, y=555)
            # except Exception as e:
            #     print(e)

    def create_connection(self):
        create_ovpn_configuration = ParseConfigurationFile()
        create_ovpn_configuration.start(self.selection)
        self.connect.start_connection()
        time.sleep(2)
        self.connect.set_options()
        print(self.pid)
        self.connect_button.config(text="Disconnect", command=self.disconnect)

    def connect_button_event_as_thread(self):
        threading.Thread(target=self.buttonEvent, args=()).start()

    def disconnect(self):
        self.connect.disconnect()
        self.connect_button.config(text="Connect", command=self.connect_button_event_as_thread)
