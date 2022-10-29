from pydoc_data.topics import topics
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
    QTableWidgetItem,
)

import sys

from .const import *

from functions.pomodoro.ui_pomodoro import Ui_PomodoroPage, Ui_SettingsWindow

from enum import Enum

from ..db_main_operations import DBMainOperations

class Mode(Enum):
    work = 1
    short_rest = 2
    long_rest = 3

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

        self.settingsWindow = QtWidgets.QMainWindow()
        self.ui_settingsWindow = Ui_SettingsWindow()
        self.ui_settingsWindow.setupUi(self.settingsWindow)
        global settingsWidgets
        settingsWidgets = self.ui_settingsWindow

        self.setupConnections()

        self.load_data_in_table()

        print('test')

    def setupVariables(self):
        self.settings = QSettings()
        self.workEndTime = QTime(
            int(self.settings.value(workHoursKey, 0)),
            int(self.settings.value(workMinutesKey, 25)),
            int(self.settings.value(workSecondsKey, 0)),
        )
        self.restEndTime = QTime(
            int(self.settings.value(restHoursKey, 0)),
            int(self.settings.value(restMinutesKey, 5)),
            int(self.settings.value(restSecondsKey, 0)),
        )
        self.timeFormat = "hh:mm:ss"
        self.time = self.workEndTime
        self.workTime = QTime(0, 0, 0, 0)
        self.restTime = QTime(0, 0, 0, 0)
        self.totalTime = QTime(0, 0, 0, 0)
        self.currentMode = Mode.work
        self.maxRepetitions = -1
        self.currentRepetitions = 0

        self.activeMode = "rest"

        ## Progress bar variables
        self.workSecondPercent = 1/(25*60/100)
        self.restSecondPercent =  1/(5*60/100)
        self.progressValue = 0
    
    def setupConnections(self):
        widgets.btnAction.clicked.connect(self.startTimer)
        widgets.btnReset.clicked.connect(self.resetTimer)
        widgets.btnSettings.clicked.connect(self.openSettingsWindow)
        settingsWidgets.btnChangeSettings.clicked.connect(self.makeSettingsChanges)

        widgets.timeDisplay.display(self.time.toString(self.timeFormat))

        """ Create tablewidget connections """
        widgets.tblTasks.cellDoubleClicked.connect(self.markTaskAsFinished)
        widgets.tblTasks.cellClicked.connect(self.showTaskInLabel)

    def leaveEvent(self, event):
        super(PomodoroMainPage, self).leaveEvent(event)

    def startTimer(self):
        try:
            if not self.timer.isActive():
                self.createTimer()
        except:
            self.createTimer()
        self.load_data_in_table()

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
            self.time = self.workEndTime
            self.displayTime()
            self.progressValue = 0
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
        self.time = self.time.addSecs(-1)
        self.totalTime = self.totalTime.addSecs(-1)
        
        ## Progress bar logic
        self.progressValue += self.workSecondPercent
        widgets.progressBar.setValue(self.progressValue)
        print(f'progress: {self.progressValue}')

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

    ############## Settings Window

    def openSettingsWindow(self):
        self.settingsWindow.show()

    def makeSettingsChanges(self):
        print('changing...')
        self.settings.setValue(workHoursKey, settingsWidgets.workHoursSpinBox.value())
        self.settings.setValue(
            workMinutesKey,
            settingsWidgets.workMinutesSpinBox.value(),
        )
        self.settings.setValue(
            workSecondsKey,
            settingsWidgets.workSecondsSpinBox.value(),
        )
        self.settings.setValue(restHoursKey, settingsWidgets.restHoursSpinBox.value())
        self.settings.setValue(
            restMinutesKey,
            settingsWidgets.restMinutesSpinBox.value(),
        )
        self.settings.setValue(
            restSecondsKey,
            settingsWidgets.restSecondsSpinBox.value(),
        )

        self.workEndTime = QTime(
            int(self.settings.value(workHoursKey, settingsWidgets.workHoursSpinBox.value())),
            int(self.settings.value(workMinutesKey, settingsWidgets.workMinutesSpinBox.value())),
            int(self.settings.value(workSecondsKey, settingsWidgets.workSecondsSpinBox.value())),
        )
        self.restEndTime = QTime(
            int(self.settings.value(workHoursKey, settingsWidgets.restHoursSpinBox.value())),
            int(self.settings.value(workMinutesKey, settingsWidgets.restMinutesSpinBox.value())),
            int(self.settings.value(workSecondsKey, settingsWidgets.restSecondsSpinBox.value())),
        )

        self.workSecondPercent = 1/(workMinutesKey*60/100)
        self.restSecondPercent =  1/(restMinutesKey*60/100)
        self.progressValue = 0

        self.settingsWindow.close()
        self.resetTimer()

    #### TASKS

    def load_data_in_table(self):
        print("\n ##########################################################")
        widgets.tblTasks.clearContents()

        with DBMainOperations() as db:
            qry = """SELECT COUNT(*) FROM tasks WHERE status != 'Completed';
            """
            count = db.cursor.execute(qry).fetchone()[0]
            self.row_tasks_count = count
            widgets.tblTasks.setRowCount(self.row_tasks_count)
            
            self.topics = db.cursor.execute("SELECT * FROM topics").fetchall()

            ## Show just no completed tasks
            qry = """SELECT task_name, topic_id FROM tasks
            WHERE status != 'Finalizada' ORDER BY start_date;"""
            results = db.cursor.execute(qry).fetchall()
            
            try:
                tablerow = 0
                for row in results:
                    widgets.tblTasks.setRowHeight(tablerow, 40)
                    widgets.tblTasks.setItem(tablerow, 0, QTableWidgetItem(row[0]))  #row[0] = task_name
                    widgets.tblTasks.setItem(tablerow, 1, QTableWidgetItem(self.topics[row[1]][1])) #row[1] = topic_id
                    tablerow += 1
                widgets.tblTasks.setRowHeight(tablerow, 40)
            except Exception:
                print('ERROR')

    def markTaskAsFinished(self, row, col):
        item = widgets.tblTasks.item(row, 0)
        font = widgets.tblTasks.item(row, 0).font()
        font.setStrikeOut(False if item.font().strikeOut() else True)
        item.setFont(font)

        query_update = f"UPDATE tasks SET status = 'Finalizada' WHERE task_name = '{item.text()}'"
        with DBMainOperations() as db:
            db.cursor.execute(query_update)

    def showTaskInLabel(self, row, col):
        item = widgets.tblTasks.item(row, col)
        widgets.lblTask.setText(item.text())

if __name__ == "__main__":
    app = QApplication([])
    widget = PomodoroMainPage
    widget.show()
    sys.exit(app.exec())