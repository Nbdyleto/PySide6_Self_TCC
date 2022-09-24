import os
from pathlib import Path
import sys

from .ui_pomodoro import *

from PySide6 import QtCore, QtGui, QtWidgets
from PySide6.QtWidgets import QWidget, QApplication

class PomodoroMainPage(QWidget):
    def __init__(self):
        super(PomodoroMainPage, self).__init__()
        self.ui = Ui_Pomodoro()
        self.ui.setupUi(self)