from random import choice
from PySide6 import QtCore, QtGui, QtWidgets
from PySide6.QtWidgets import QWidget, QApplication
from PySide6.QtCore import QSettings, QTime

from PySide6.QtCore import Qt, QTime, QTimer, QSettings, QDir
from PySide6.QtWidgets import (
    QApplication,
    QComboBox,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QSpinBox,
    QVBoxLayout,
    QWidget,
)

import sys

from .const import *

from functions.pomodoro.ui_pomodoro import Ui_PomodoroPage, Ui_SettingsWindow

from enum import Enum

class Mode(Enum):
    work = 1
    rest = 2

class Status(Enum):
    workFinished = 1
    restFinished = 2
    repetitionsReached = 3

class PomodoroMainPage(QWidget):
    def __init__(self):
        super(PomodoroMainPage, self).__init__()
        self.setupVariables()
        self.ui = Ui_PomodoroPage()
        self.ui.setupUi(self)

        global widgets
        widgets = self.ui

        self.setupConnections()

    def setupVariables(self):
        settings = QSettings()
        self.workEndTime = QTime(
            int(settings.value(workHoursKey, 0)),
            int(settings.value(workMinutesKey, 25)),
            int(settings.value(workSecondsKey, 0)),
        )
        self.restEndTime = QTime(
            int(settings.value(restHoursKey, 0)),
            int(settings.value(restMinutesKey, 5)),
            int(settings.value(restSecondsKey, 0)),
        )
        self.timeFormat = "hh:mm:ss"
        self.time = QTime(0, 0, 0, 0)
        self.workTime = QTime(0, 0, 0, 0)
        self.restTime = QTime(0, 0, 0, 0)
        self.totalTime = QTime(0, 0, 0, 0)
        self.currentMode = Mode.work
        self.maxRepetitions = -1
        self.currentRepetitions = 0

        self.activeMode = "rest"
    
    def setupConnections(self):
        widgets.btnAction.clicked.connect(self.startTimer)
        widgets.btnReset.clicked.connect(self.resetTimer)
        widgets.btnSettings.clicked.connect(self.openSettingsWindow)

    def leaveEvent(self, event):
        super(PomodoroMainPage, self).leaveEvent(event)

    def closeEvent(self, event):
        super(PomodoroMainPage, self).closeEvent(event)
        settings = QSettings()
        settings.setValue(workHoursKey, 0)
        settings.setValue(
            workMinutesKey,
            25,
        )
        settings.setValue(
            workSecondsKey,
            0,
        )
        settings.setValue(restHoursKey, 0)
        settings.setValue(
            restMinutesKey,
            5,
        )
        settings.setValue(
            restSecondsKey,
            0,
        )

    def startTimer(self):
        try:
            if not self.timer.isActive():
                self.createTimer()
        except:
            self.createTimer()

    def createTimer(self):
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.updateTime)
        self.timer.timeout.connect(self.maybeChangeMode)
        self.timer.setInterval(1000)
        self.timer.setSingleShot(False)
        self.timer.start()

    def pauseTimer(self):
        try:
            self.timer.stop()
            self.timer.disconnect()
        except:
            pass

    def resetTimer(self):
        try:
            self.pauseTimer()
            self.time = QTime(0, 0, 0, 0)
            self.displayTime()
        except:
            pass

    def maybeStartTimer(self):
        if self.currentRepetitions != self.maxRepetitions:
            self.startTimer()
            started = True
        else:
            self.currentRepetitions = 0
            started = False
        return started

    def updateCurrentMode(self, mode: str):
        self.currentMode = Mode.work if mode == "work" else Mode.rest

    def updateTime(self):
        self.time = self.time.addSecs(1)
        self.totalTime = self.totalTime.addSecs(1)
        if self.activeMode == "work":
            self.workTime = self.workTime.addSecs(1)
        else:
            self.restTime = self.restTime.addSecs(1)
        self.displayTime()

    def updateMaxRepetitions(self, value):
        if value == 0:
            self.currentRepetitions = 0
            self.maxRepetitions = -1
        else:
            self.maxRepetitions = 2 * value

    def maybeChangeMode(self):
        if self.currentMode is Mode.work and self.time >= self.workEndTime:
            self.resetTimer()
            self.activeMode = "rest"
            self.incrementCurrentRepetitions()
            started = self.maybeStartTimer()
            self.showWindowMessage(
                Status.workFinished if started else Status.repetitionsReached
            )
        elif self.currentMode is Mode.rest and self.time >= self.restEndTime:
            self.resetTimer()
            self.activeMode = "work"
            self.incrementCurrentRepetitions()
            started = self.maybeStartTimer()
            self.showWindowMessage(
                Status.restFinished if started else Status.repetitionsReached
            )

    def incrementCurrentRepetitions(self):
        if self.maxRepetitions > 0:
            self.currentRepetitions += 1

    def displayTime(self):
        widgets.timeDisplay.display(self.time.toString(self.timeFormat))

    def openSettingsWindow(self):
        self.settingsWindow = QtWidgets.QMainWindow()
        self.ui_settingsWindow = Ui_SettingsWindow()
        self.ui_settingsWindow.setupUi(self.settingsWindow)
        self.settingsWindow.show()

    
if __name__ == "__main__":
    app = QApplication([])
    widget = PomodoroMainPage
    widget.show()
    sys.exit(app.exec_())