from tkinter import *
import servers




gui = Tk()
gui.resizable(False, False)
gui.title('IPVanish Client')
gui.geometry('320x500')

img = PhotoImage (file = 'ipvanish-text-logo-white.png')
canvas = Canvas (gui, width = 320, height = 500 ) #image size
canvas.create_image(5, 5, anchor = NW, image = img)
canvas.pack()

nvariable = StringVar(gui)
nvariable.set(servers.nations()[0])

cvariable = StringVar(gui)
cvariable.set('')


Nlabel= Label (gui, text='Choose Country', font=('Helvetica',18))
Nlabel.place(x=52,y=80)
nations = OptionMenu(gui, nvariable, *servers.nations())
nations.place(x=52,y=120)
nations.config(width=20)

servers.nations()[nvariable.get()]

Clabel= Label (gui, text='Choose City', font=('Helvetica',18))
Clabel.place(x=52,y=180)
cities = OptionMenu(gui, cvariable, '')
cities.place(x=52,y=210)
cities.config(width=20)


gui.mainloop()

