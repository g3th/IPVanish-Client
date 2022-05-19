import os
import requests
import subprocess
import time

print('\x1bc')

ctr=0 ; progress='#';files=[]; path='/home'

page='https://www.ipvanish.com/software/configs/'

req=requests.get(page)

for line in req.text.splitlines():

	if "ipvanish" in line:
		files.append(line.split("href=")[1].split('"')[1])

directory_ = subprocess.check_output("find /home -type d -name 'IPVanish_Client'", shell = True)

directory = str(directory_).strip("b'").strip("\\n")

print("Client installed in: " + directory + "\n")

if 'configs' not in os.listdir(directory):
	
	print('Created "configs" directory \n')

	os.mkdir (directory + "/configs")

print("Downloading Config files")

while ctr < 3: #len(files):

	print('\x1bc');print("Downloading Config files: %",end='')
	print(int(ctr/len(files)))
	subprocess.check_call(['wget "'+page+files[ctr]+'" -P '+directory+'/configs/'])
#	req=requests.get(page+files[ctr])
#	open(directory+"/configs/"+files[ctr],'wb').write(req.content)
	ctr +=1

#while ctr < 3: # len(servers):
#	print("\x3d")	
#	ctr +=1
