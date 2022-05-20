import os

#how many files?


path='/home/user/Desktop/IPVanish-Client/configs/'

print(len(os.listdir(path)))

if len(os.listdir(path)) > 1:
	print("more than 1 file")

