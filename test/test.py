import os, sys
import subprocess
import shlex
import servers

#how many files?

def files():

	path='/home/'

	print(len(os.listdir(path)))

	if len(os.listdir(path)) > 1:
		print("more than 1 file")

def termios():

	# stty -a

	termios = subprocess.run(shlex.split('stty -a'))

	print(termios) # termios settings

	termios = subprocess.run(shlex.split('stty -echo'))

	while True:

		option = input ('Testing Input:')

		repeat = input ('\n\nRepeat Input:')
	
		if option == repeat:

			print ('\n\nInput Matches - Returning Input "' + option + '"\n')
			print ('Resetting terminal echo')
			break
		
		else:

			print('Does not match')


	subprocess.run(shlex.split('stty echo'))

def sortList():
	
	with open('countries','a') as sort:
		for nation in servers.nations():
			sort.write(nation+", ")
	sort.close()
		
sortList()



