import os
import subprocess
import shlex
import modules.dlconfig as config



def userPass():

	if 'credentials' in os.listdir(config.create_dirs()[0]):

		print('Credentials exist\n')
		repeat='';password=''
	else:
	
		command = shlex.split('stty -echo')

		email = input('Credentials - email:')

		while True:

			subprocess.run(command)

			password = input ('\n(echo off) Credentials - password: ')

			repeat = input ('\nRepeat - password: ')

			if password == repeat:

				with open(config.create_dirs()[0]+'/credentials','a') as credentials:

					credentials.write(email+"\n")
					credentials.write(password)
				repeat='';password=''
				credentials.close()

				break
		
			else:

				print('Does not match')


		subprocess.run(shlex.split('stty echo'),shell=False)
