import signal
import threading
import subprocess
import modules.dlconfig as config
from subprocess import PIPE
from modules.servers import nations as n
from modules.servers import nations_as_tags
from modules.servers import cities as c
from pathlib import Path
from tkinter import *
from tkinter import ttk
from random import randint
import time
import os

class TabsLists:

    def __init__(self, root):

        self.process_pid = None
        self.openvpn_command = None
        self.ipvanish_dns = ['198.18.0.1', '198.18.0.2']
        self.default_gateway = '192.168.0.1'
        self.loopback = '192.168.0.1'
        self.current_interface = []
        self.user_name = None
        self.password = None
        self.sudo_password = None
        self.user_name_label = None
        self.password_label = None
        self.displayed_user_name = None
        self.displayed_password = None
        self.random_server = None
        self.extract_selection_index = None
        self.selection = None
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
            self.no_credentials()
        else:
            for credential in self.credentials:
                with open(self.configuration_files_path + "/credentials", 'a') as write_creds:
                    write_creds.write(credential + "\n")
                write_creds.close()
            self.display_stored_credentials(self.credentials[0], self.credentials[1])

    def store_sudo_password(self):
        self.sudo_password = self.sudo_password_box.get()
        if self.sudo_password == "":
            self.no_sudo_password()
        else:
            self.sudo_password_box.destroy()
            display_sudo_password = Label(self.tab_three, text="*" * len(self.sudo_password))
            display_sudo_password.place(x=55, y=220)

    def no_sudo_password(self):
        no_sudo_password_error = Toplevel(self.notebook)
        no_sudo_password_error.geometry("220x70")
        no_sudo_password_error.resizable(False, False)
        no_sudo_password_error.title("Error")
        Label(no_sudo_password_error, font=("Arial", 13), text='Please Enter a Password').place(x=14, y=8)

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

    def no_selection(self):
        nothing_selected_error = Toplevel(self.notebook)
        nothing_selected_error.geometry("160x70")
        nothing_selected_error.resizable(False, False)
        nothing_selected_error.title("Error")
        Label(nothing_selected_error, font=("Arial", 13), text='Please Select \na Server').place(x=14, y=8)

    def no_credentials(self):
        no_credentials_error = Toplevel(self.notebook)
        no_credentials_error.geometry("160x70")
        no_credentials_error.resizable(False, False)
        no_credentials_error.title("Error")
        Label(no_credentials_error, font=("Arial", 13), text='Please Enter \nUser Credentials').place(x=14, y=8)

    def buttonEvent(self):
        if not self.credentials:
            self.no_credentials()
        else:
            # try:
            selected = self.notebook.index('current')
            match selected:
                case 0:
                    self.extract_selection_index = str(self.list_of_nations.curselection()).split("(")[1].strip(
                        ",)")
                    self.selection = nations_as_tags[int(self.extract_selection_index)]
                case 1:
                    self.extract_selection_index = str(self.list_of_cities.curselection()).split("(")[1].strip(",)")
                    self.selection = c[int(self.extract_selection_index)]
            if self.sudo_password is None:
                self.no_sudo_password()
            else:
                self.connect()
                self.button_label['text'] = 'Connected to ' + self.selection + ' server\n'
                self.button_label.place(x=80, y=555)
            # except Exception as e:
            #     print(e)

    def connect(self):
        filelist = []
        for i in os.listdir(self.configuration_files_path):
            if self.selection in i:
                filelist.append(i)
        length = len(filelist) - 1
        random_server_dir = filelist[randint(0, length)]
        original_configuration_file_lines = open(self.configuration_files_path + "/" + random_server_dir).readlines()
        with open(self.configuration_files_path + "/conn.ovpn", 'w') as create_ovpn_configuration_file:
            for i in original_configuration_file_lines:
                if "auth-user-pass" in i:
                    create_ovpn_configuration_file.write(
                        "auth-user-pass {}/credentials\n\n".format(self.configuration_files_path))
                elif "ca ca.ipvanish.com.crt" in i:
                    create_ovpn_configuration_file.write(
                        "ca {}/ca.ipvanish.com.crt\n\n".format(self.configuration_files_path))
                elif "keysize 256" in i:
                    create_ovpn_configuration_file.write("")
                else:
                    create_ovpn_configuration_file.write(i + "\n")
        self.connect_button.config(text="Disconnect", command=self.disconnect)
        self.set_resolved_dns_and_establish_connection()

    def connect_button_event_as_thread(self):
        threading.Thread(target=self.buttonEvent, args=()).start()

    def disconnect(self):
        os.kill(self.process_pid, signal.SIGINT)
        resolved_status_command = ['sudo', '-S', 'resolvectl', 'status']
        resolved_status_output = subprocess.Popen(resolved_status_command, shell=False, stdin=PIPE, stdout=PIPE, encoding='utf-8').communicate(input=self.sudo_password)
        output = resolved_status_output[0].split("\n")
        for i in output:
            if "Link" in i:
                self.current_interface.append(i.split("(")[1].split(")")[0])
        for interface in self.current_interface:
            disable_ipv6 = ['sudo',  '-S', 'sysctl', 'net.ipv6.conf.all.disable_ipv6=0']
            set_default_route = ['sudo',  '-S', 'resolvectl', 'default-route', interface, 'true']
            set_llmnr = ['sudo',  '-S', 'resolvectl', 'llmnr', interface, 'true']
            set_mdns = ['sudo',  '-S', 'resolvectl', 'mdns', interface, 'true']
            resolved_set_dns_command = ['sudo', '-S', 'resolvectl', 'dns', interface, self.default_gateway]
            subprocess.Popen(disable_ipv6, shell=False,
                             encoding='utf-8').communicate(input=self.sudo_password)

            subprocess.Popen(resolved_set_dns_command, shell=False,
                             encoding='utf-8').communicate(input=self.sudo_password)

            subprocess.Popen(set_default_route, shell=False,
                             encoding='utf-8').communicate(input=self.sudo_password)

            subprocess.Popen(set_llmnr, shell=False,
                             encoding='utf-8').communicate(input=self.sudo_password)

            subprocess.Popen(set_mdns, shell=False,
                             encoding='utf-8').communicate(input=self.sudo_password)
            self.connect_button.config(text="Connect", command=self.connect_button_event_as_thread)

    def ovpn_connection(self):
        openvpn_command_as_list = ['sudo', '-S', 'openvpn', '--config', self.configuration_files_path + "/conn.ovpn"]
        self.openvpn_command = subprocess.Popen(openvpn_command_as_list, shell=False, stdin=PIPE,
                                                encoding='utf-8')
        self.openvpn_command.communicate(input=self.sudo_password)

    def ovpn_connection_thread(self):
        threading.Thread(target=self.ovpn_connection, args=()).start()
        time.sleep(5)
        set_tunnel_dns = ['sudo', '-S', 'resolvectl', 'dns', 'tun0', self.ipvanish_dns[0], self.ipvanish_dns[1]]
        set_default_route = ['sudo', '-S', 'resolvectl', 'default-route', 'tun0', 'true']
        subprocess.Popen(set_default_route, shell=False,
                         encoding='utf-8').communicate(input=self.sudo_password)
        subprocess.Popen(set_tunnel_dns, shell=False,
                         encoding='utf-8').communicate(input=self.sudo_password)
        self.process_pid = self.openvpn_command.pid

    def set_resolved_dns_and_establish_connection(self):
        resolved_status_command = ['sudo', '-S', 'resolvectl', 'status']
        resolved_status_output = subprocess.Popen(resolved_status_command, shell=False, stdin=PIPE, stdout=PIPE, encoding='utf-8').communicate(input=self.sudo_password)
        output = resolved_status_output[0].split("\n")
        self.ovpn_connection_thread()
        time.sleep(2)
        for i in output:
            if "Link" in i:
                self.current_interface.append(i.split("(")[1].split(")")[0])
        for interface in self.current_interface:
            disable_ipv6 = ['sudo',  '-S', 'sysctl', 'net.ipv6.conf.all.disable_ipv6=1']
            set_default_route = ['sudo',  '-S', 'resolvectl', 'default-route', interface, 'false']
            set_llmnr = ['sudo',  '-S', 'resolvectl', 'llmnr', interface, 'false']
            set_mdns = ['sudo',  '-S', 'resolvectl', 'mdns', interface, 'false']
            resolved_set_dns_command = ['sudo', '-S', 'resolvectl', 'dns', interface, self.ipvanish_dns[0], self.ipvanish_dns[1]]
            subprocess.Popen(disable_ipv6, shell=False,
                             encoding='utf-8').communicate(input=self.sudo_password)

            subprocess.Popen(resolved_set_dns_command, shell=False,
                             encoding='utf-8').communicate(input=self.sudo_password)

            subprocess.Popen(set_default_route, shell=False,
                             encoding='utf-8').communicate(input=self.sudo_password)

            subprocess.Popen(set_llmnr, shell=False,
                             encoding='utf-8').communicate(input=self.sudo_password)

            subprocess.Popen(set_mdns, shell=False,
                             encoding='utf-8').communicate(input=self.sudo_password)

