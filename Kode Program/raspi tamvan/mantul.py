from PyQt5.QtWidgets import QMainWindow,QApplication,QWidget,QPushButton,QAction,QLineEdit,QMessageBox
import sys
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot
class App(QMainWindow):
       def __init__(self):
               super().__init__()
               self.title='Hello, world!'
               self.left=10
               self.top=10
               self.width=400
               self.height=140
               self.initUI()
       def initUI(self):
               self.setWindowTitle(self.title)
               self.setGeometry(self.left,self.top,self.width,self.height)
               self.textbox=QLineEdit(self)
               self.textbox.move(30,30)
               self.textbox.resize(280,40)
               self.button=QPushButton('Click me',self)
               self.button.move(15,85)
               self.button.clicked.connect(self.on_click)
               self.show()
       @pyqtSlot()
       def on_click(self):
               textboxValue=self.textbox.text()
               QMessageBox.question(self, 'Hello, world!', "Confirm: "+textboxValue,                                                                            QMessageBox.Ok, QMessageBox.Ok)
               self.textbox.setText("...")
if __name__=='__main__':
       app=QApplication(sys.argv)
       ex=App()