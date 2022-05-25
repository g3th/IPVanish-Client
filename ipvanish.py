import os
import subprocess
import shlex
import modules.dlconfig as config
import modules.userpass as credentials

print("\x1bc")

setup = config.dlconfigs()

print('Checking Directories...\n')

setup.check_dirs()

setup.create_dirs()

if setup.create_dirs()[2] == 1:

	print('Client found in: '+ setup.create_dirs()[1])

setup.subprocess()

credentials.userPass()

