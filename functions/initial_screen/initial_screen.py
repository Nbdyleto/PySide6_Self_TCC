from PySide6 import QtCore, QtGui, QtWidgets

from functions.initial_screen.ui_initial_screen import Ui_InitialScreen

class InitialMainPage(QtWidgets.QWidget):
    def __init__(self):
        super(InitialMainPage, self).__init__()
        self.ui = Ui_InitialScreen()
        self.ui.setupUi(self)
        global widgets
        widgets = self.ui
        #self.setupVariables()
        #self.setupConnections()
        self.setupWidgets()
    
    def setupWidgets(self):
        #image = QtGui.QImage('bem_vindo.jpg)')
        #pp = QtGui.QPixmap.fromImage(image)
        #self.ui.label.setPixMap(pp)
        #self.ui.label.setScaledContents(True)
        self.ui.widget.setStyleSheet(u"""
        border-image: url(:/images/images/images/initial/Flashcards.png);
        background-position: center;
        background-repeat: no-repeat;
        stretch stretch;"""
        )
        self.ui.widget_2.setStyleSheet(u"""
        border-image: url(:/images/images/images/initial/Tarefas.png);
        background-position: center;
        background-repeat: no-repeat;
        stretch stretch;"""
        )
        self.ui.widget_3.setStyleSheet(u"""
        border-image: url(:/images/images/images/initial/Pomodoro.png);
        background-position: center;
        background-repeat: no-repeat;
        stretch stretch;"""
        )
        self.ui.widget_4.setStyleSheet(u"""
        border-image: url(:/images/images/images/initial/Ver_Progresso.png);
        background-position: center;
        background-repeat: no-repeat;
        stretch stretch;"""
        )