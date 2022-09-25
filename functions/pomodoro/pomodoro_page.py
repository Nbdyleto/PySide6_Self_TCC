from functions.pomodoro.circular_progress import SECONDS_TOTAL
from functions.pomodoro.pomodoro_timer import PomodoroTimer
from functions.pomodoro.settings import CherryTomatoSettings
from functions.pomodoro.timer_proxy import AbstractTimerProxy, PomodoroTimerProxy
from functions.pomodoro.utils import CommandExecutor
import widgets

from .ui_pomodoro import *

from PySide6 import QtCore, QtGui, QtWidgets
from PySide6.QtWidgets import QWidget, QApplication

class PomodoroMainPage(QWidget):
    def __init__(self, timerProxy: AbstractTimerProxy):
        super(PomodoroMainPage, self).__init__()
        self.ui = Ui_Pomodoro()
        self.ui.setupUi(self)

        # window.py
        self.timerProxy = timerProxy

        self.ui.button.clicked.connect(self.timerProxy.onAction)
        self.timerProxy.onChange.connect(self.display)
        self.timerProxy.finished.connect(self.setFocusOnWindowAndPlayNotification)

        self.display()
    
    @QtCore.Slot(name='display')
    def display(self):
        #self.progress.useSystemFont = self.settings.useSystemFont
        #self.progress.setFormat(self.timerProxy.getUpperText())
        #self.progress.setSecondFormat(self.timerProxy.getBottomText())
        self.ui.progress.set_value(self.timerProxy.getProgress())
        self.changeButtonState()
        print(self.ui.progress.value)

    def changeButtonState(self):
        if not self.timerProxy.isRunning():
            self.ui.button.setImage('play.png')
        else:
            self.ui.button.setImage('stop.png')