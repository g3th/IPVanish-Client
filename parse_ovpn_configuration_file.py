import os
from modules.servers import n_america
from modules.servers import europe
from modules.servers import nations_dict
from random import randint
from pathlib import Path


class ParseConfigurationFile:

    def __init__(self):
        self.configuration_files_path = str(Path(__file__).parent) + "/configs"
        self.result = nations_dict
        self.filelist = []

    def start(self, selection, tab_index):
        self.larger_area_check(selection)
        match tab_index:
            case 0:
                for i in os.listdir(self.configuration_files_path):
                    if self.result[selection] in i:
                        self.filelist.append(i)
            case 1:
                for i in os.listdir(self.configuration_files_path):
                    if selection in i:
                        self.filelist.append(i)
        length = len(self.filelist) - 1
        random_server_dir = self.filelist[randint(0, length)]
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

    def larger_area_check(self, selection):
        if selection == "North America":
            for i in os.listdir(self.configuration_files_path):
                for j in n_america:
                    if j in i:
                        self.filelist.append(i)
        if selection == "Europe":
            for i in os.listdir(self.configuration_files_path):
                for j in europe:
                    if j in i:
                        self.filelist.append(i)
