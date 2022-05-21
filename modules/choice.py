from tkinter import *

CredText='No Credential Stored'

class mainWindow:
	
	def __init__(self , gui):

		self.gui = gui
		gui.resizable(False, False)
		gui.title('IPVanish Client')
		gui.geometry('320x500')

		img = PhotoImage (file = 'ipvanish-text-logo-white.png')
		canvas = Canvas (gui, width = 320, height = 500 ) #image size
		canvas.create_image(5, 5, anchor = NW, image = img)
		canvas.pack()

		credentialText = Label(gui, text = CredText, font=('Helvetica',15))
		credentialText.place(x = 58, y = 72)

		eLabel = Label(gui, text="Enter Email", font=('Helvetica',10))
		eLabel.place(x = 50, y = 150)

		email = Entry (gui, font=('Helvetica',10),width=30)
		email.place(x = 50, y = 180)

		pLabel = Label(gui,text="Enter Password", font=('Helvetica',10))
		pLabel.place(x = 50, y = 220)

		password = Entry(gui,show="*", font=('Helvetica',10), width=30)
		password.place(x = 50, y = 250)

		btn = Button(gui, text = 'Store Credentials', bd = '1', command = dstry)
		btn.pack()
		btn.place(x=85, y=320)

		def dstry():

			eLabel.destroy()
			email.destroy()
			pLabel.destroy()
			password.destroy()


root = Tk()
window = mainWindow(root)
root.mainloop()
