import threading
import queue
from concurrent.futures import ThreadPoolExecutor
import os, sys
from random import randint
import subprocess
import shlex
import servers
import glob


# how many files?

def files():
    path = '/home/'

    print(len(os.listdir(path)))

    if len(os.listdir(path)) > 1:
        print("more than 1 file")


# Easy echo-off for passwords
# One line, unlike retarded explanations on Stackoverflow or Google

def termios():
    # stty -a

    termios = subprocess.run(shlex.split('stty -a'), shell=False)

    print(termios)  # termios settings

    termios = subprocess.run(shlex.split('stty -echo'), shell=False)  # echo off, that's all

    while True:

        option = input('Testing Input:')

        repeat = input('\n\nRepeat Input:')

        if option == repeat:

            print('\n\nInput Matches - Returning Input "' + option + '"\n')
            print('Resetting terminal echo')
            break

        else:

            print('Does not match')

    subprocess.run(shlex.split('stty echo'), shell=False)  # echo on, one line, not a 10 line function


# ...retards

def sortList():
    with open('countries', 'a') as sort:
        for nation in servers.nations():
            sort.write(nation + ", ")
    sort.close()


def pfiles():
    path = ''

    filelist = []

    city = input("City: ")
    print(city)

    for i in glob.glob(path + "*" + str(city) + "*"):
        filelist.append(i)

    filelist = sorted(filelist)

    print(*filelist, sep="\n")

def interfaces():
    network_interfaces_list = os.listdir("/sys/class/net")
    for interface in network_interfaces_list:
        commands_as_list_of_lists = [['sudo', '-S', 'sysctl', 'net.ipv6.conf.all.disable_ipv6=1'],
                                     ['sudo', '-S', 'resolvectl', 'default-route', interface, 'false'],
                                     ['sudo', '-S', 'resolvectl', 'llmnr', interface, 'false'],
                                     ['sudo', '-S', 'resolvectl', 'mdns', interface, 'false'],
                                     ['sudo', '-S', 'resolvectl', 'dns', interface, '0']]
        for command in commands_as_list_of_lists:
            if "tun0" not in interface and interface != "lo":
                print(command)

def first():
    f = queue.Queue()
    print("1")
def second():
    s = queue.Queue()
    print("2")

for i in range(2):
    t = threading.Thread()

