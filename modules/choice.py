import os
import servers
import sys
from PyQt5 import QtWidgets, QtGui, QtCore



def basicWindow():
    	app = QtWidgets.QApplication(sys.argv)
    	GUI = QtWidgets.QWidget()
    	GUI.setGeometry(450, 200, 330, 420)
    	Logo = QtWidgets.QLabel(GUI)
    	Logo.setPixmap(QtGui.QPixmap('ipvanish.jpg'))
    	GUI.setWindowIcon(QtGui.QIcon("ipvanish.png"))
    	GUI.setWindowTitle('IP Vanish Linux App')
    	GUI.show()
    	sys.exit(app.exec_())

basicWindow()
