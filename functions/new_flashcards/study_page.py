from PySide6 import QtCore, QtGui, QtWidgets

from functions.new_flashcards.ui_study import Ui_StudyPage

class MainStudyPage(QtWidgets.QWidget):
    def __init__(self):
        super(MainStudyPage, self).__init__()
        self.ui = Ui_StudyPage()
        self.ui.setupUi(self)

        global widgets
        widgets = self.ui