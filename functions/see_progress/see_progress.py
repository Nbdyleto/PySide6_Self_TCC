from PySide6 import QtCore, QtGui, QtWidgets

from functions.see_progress.ui_see_progress import Ui_SeeProgressPage

class SeeProgressMainPage(QtWidgets.QWidget):
    def __init__(self):
        super(SeeProgressMainPage, self).__init__()
        self.ui = Ui_SeeProgressPage()
        self.ui.setupUi(self)