import sys
from PyQt5 import QtCore, QtGui, QtWidgets

class setup_UI(object):
    def setupUi(self, window):
        window.setObjectName("PyQt5 Window")
        window.resize(300, 400)
        
        self.Button = QtWidgets.QPushButton(window)
        self.Button.setGeometry(QtCore.QRect(100, 70, 93, 28))  
        self.Button.setObjectName("Button")
        
        self.Label = QtWidgets.QLabel(window)
        self.Label.setGeometry(QtCore.QRect(75, 149, 151, 31))  
        self.Label.setObjectName("Label")
        
        self.retranslateUi(window)
        QtCore.QMetaObject.connectSlotsByName(window)
        
        self.Button.clicked.connect(self.showmsg) 

    def retranslateUi(self, window):
        _translate = QtCore.QCoreApplication.translate
        window.setWindowTitle(_translate("window", "PyQt5 Window"))
        self.Button.setText(_translate("window", "Click"))
        self.Label.setText(_translate("window", ""))  

    def showmsg(self):
        self.Label.setText("You clicked me")

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
 
    MainWindow = QtWidgets.QMainWindow()
    ui = setup_UI()
 
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
