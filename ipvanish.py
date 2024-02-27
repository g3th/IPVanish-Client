#!/usr/bin/python3

from tabs import TabsLists
from pathlib import Path
from tkinter import *
from tkinter import ttk
from PIL import ImageTk


class IPVanishGUI:

    def __init__(self, title):
        self.directory = str(Path(__file__).parent)
        self.IPVanish = Tk()
        self.IPVanish.title(title)
        self.IPVanish.resizable(False, False)
        self.IPVanish.geometry('340x600')

    def image(self, xplace, yplace, xpos, ypos, width, height, anchor):
        image = ImageTk.PhotoImage(file=self.directory + '/assets/ipvanish-text-logo-white.png')
        canvas = Canvas(self.IPVanish, width=width, height=height)
        canvas.image = image
        canvas.create_image(xpos, ypos, anchor=anchor, image=image)
        canvas.place(x=xplace, y=yplace)

    def add_styles(self, widget, height):
        style = ttk.Style(self.IPVanish)
        style.configure(style=widget, height=height)

    def vpn_connection(self):
        TabsLists(self.IPVanish)

    def mainloop(self):
        self.IPVanish.mainloop()


if __name__ == '__main__':
    IPVanish = IPVanishGUI('IPVanish Client')
    IPVanish.image(8, 20, 5, 5, 350, 80, NW)
    IPVanish.add_styles('TNotebook', 50)
    IPVanish.vpn_connection()
    IPVanish.mainloop()
