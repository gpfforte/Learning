from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow
import sys
 
def window():
    def update():
        label.setText("Updated")
    
    def retrieve():
        print(label.text())
    def show():
        print(line.text())

    app = QApplication(sys.argv)
    win = QMainWindow()
    win.setGeometry(400,400,500,300)
    win.setWindowTitle("CodersLegacy")
 
    #.....
    label = QtWidgets.QLabel(win)
    label.setText("GUI application with PyQt5")
    label.adjustSize()
    label.move(100,100)

    button = QtWidgets.QPushButton(win)
    button.clicked.connect(update)
    button.setText("Update Button")
    button.move(100,150)
    
    button2 = QtWidgets.QPushButton(win)
    button2.clicked.connect(retrieve)
    button2.setText("Retrieve Button")
    button2.move(100,200)
    #.....
    line = QtWidgets.QLineEdit(win)
    line.move(300,80)

    line2 = QtWidgets.QLineEdit(win)
    line2.move(300,50)
    line2.setEchoMode(QtWidgets.QLineEdit.Password)

    button3 = QtWidgets.QPushButton(win)
    button3.setText("Submit")
    button3.clicked.connect(show)
    button3.move(300,150)
    
    button4 = QtWidgets.QPushButton(win)
    button4.setText("Clear")
    button4.clicked.connect(line.clear)
    button4.move(300,220)


    win.show()
    sys.exit(app.exec_())
     
window() 