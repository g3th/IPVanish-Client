import os
import requests
import subprocess
import shlex
import modules.dlconfig as config

print("\x1bc")

setup = config.dlconfigs()

setup.check_dirs()

print('Checking Directories...\n')

setup.create_dirs()

if setup.create_dirs()[2] == 1:

	print('Client found in: '+ setup.create_dirs()[1])

setup.subprocess()

