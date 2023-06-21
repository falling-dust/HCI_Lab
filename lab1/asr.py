from PyQt5 import QtWidgets, QtGui, QtCore, uic
from asrInterface import Ui_MainWindow
import sys


class myWindow(QtWidgets.QMainWindow):

    def __init__(self):
        super(myWindow, self).__init__()
        self.myCommand = " "
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    application = myWindow()
    application.show()
    sys.exit(app.exec())
