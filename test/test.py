import os, sys
import subprocess
import shlex
import servers
import glob

#how many files?

def files():

	path='/home/'

	print(len(os.listdir(path)))

	if len(os.listdir(path)) > 1:
		print("more than 1 file")

#Easy echo-off for passwords
#One line, unlike retarded explanations on Stackoverflow or Google

def termios():

	# stty -a

	termios = subprocess.run(shlex.split('stty -a'), shell=False)

	print(termios) # termios settings

	termios = subprocess.run(shlex.split('stty -echo'), shell=False) #echo off, that's all

	while True:

		option = input ('Testing Input:')

		repeat = input ('\n\nRepeat Input:')
	
		if option == repeat:

			print ('\n\nInput Matches - Returning Input "' + option + '"\n')
			print ('Resetting terminal echo')
			break
		
		else:

			print('Does not match')


	subprocess.run(shlex.split('stty echo'), shell=False) #echo on, one line, not a 10 line function
								#...retards

def sortList():
	
	with open('countries','a') as sort:
		for nation in servers.nations():
			sort.write(nation+", ")
	sort.close()

		
def filelists(path):

	filelist=[]

	for i in glob.glob(path):
		filelist.append(i)

	filelist = sorted(filelist)
	print(*filelist,sep="\n")
