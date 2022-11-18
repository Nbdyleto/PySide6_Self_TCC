from enum import Enum
from modules.app_functions import AppFunctions
from modules.app_settings import Settings

from modules.ui_functions import UIFunctions
from .const import *
from PySide6 import QtCore, QtGui, QtWidgets
from functions.db_main_operations import DBMainOperations

from functions.new_pomodoro.ui_pomodoro_page import Ui_Widget

class Mode(Enum):
    work = 1
    short_rest = 2
    long_rest = 3

class Status(Enum):
    workFinished = 1
    shortRestFinished = 2
    longRestFinished = 3
    repetitionsReached = 4

class NewPomodoroMainPage(QtWidgets.QWidget):
    def __init__(self):
        super(NewPomodoroMainPage, self).__init__()
        self.ui = Ui_Widget()
        self.ui.setupUi(self)
        self.setupVariables()
        self.setupConnections()
        self.setupWidgets()
        self.displayTime()

    def setupVariables(self):
        global widgets
        widgets = self.ui
        # QTime Variables
        self.settings = QtCore.QSettings()

        self.workEndTime = QtCore.QTime(
            int(self.settings.value(workHoursKey, 0)),
            int(self.settings.value(workMinutesKey, 25)),
            int(self.settings.value(workSecondsKey, 0)),
        )
        self.shortRestEndTime = QtCore.QTime(
            int(self.settings.value(shortHoursKey, 0)),
            int(self.settings.value(shortMinutesKey, 5)),
            int(self.settings.value(shortSecondsKey, 0)),
        )
        self.longRestEndTime = QtCore.QTime(
            int(self.settings.value(longHoursKey, 0)),
            int(self.settings.value(longMinutesKey, 15)),
            int(self.settings.value(longSecondsKey, 0)),
        )
        self.timeFormat = "hh:mm:ss"
        self.time = self.workEndTime
        self.workTime = QtCore.QTime(0, 0, 0, 0)
        self.restTime = QtCore.QTime(0, 0, 0, 0)
        self.totalTime = QtCore.QTime(0, 0, 0, 0)
        self.currentMode = Mode.work
        self.currentPomodoros = 1
        self.maxPomodoros = 4
        # Progress Bar Variables
        self.workSecondPercent = 1/(int(self.settings.value(workMinutesKey, 25))*60/100)
        self.shortRestSecondPercent =  1/(int(self.settings.value(shortMinutesKey, 5))*60/100)
        self.longRestSecondPercent = 1/(int(self.settings.value(longMinutesKey, 15))*60/100)
        self.progressValue = 0
        # Pallete Variables
        self.allowChangeModeManually = True

    def setupConnections(self):
        widgets.tblTasks.cellDoubleClicked.connect(self.markTaskAsFinished)
        widgets.tblTasks.cellClicked.connect(self.showTaskInLabel)

        widgets.btnPomodoro.clicked.connect(lambda: self.updateCurrentMode(Mode.work))
        widgets.btnShortRest.clicked.connect(lambda: self.updateCurrentMode(Mode.short_rest))
        widgets.btnLongRest.clicked.connect(lambda: self.updateCurrentMode(Mode.long_rest))

        widgets.btnStartTimer.clicked.connect(self.startTimer)
        widgets.btnStartTimer.clicked.connect(lambda: widgets.btnStartTimer.setDisabled(True))
        widgets.btnStartTimer.clicked.connect(lambda: widgets.btnPauseTimer.setDisabled(False))
        widgets.btnStartTimer.clicked.connect(lambda: widgets.btnResetTimer.setDisabled(False))
        widgets.btnPauseTimer.clicked.connect(self.pauseTimer)
        widgets.btnPauseTimer.clicked.connect(lambda: widgets.btnStartTimer.setDisabled(False))
        widgets.btnPauseTimer.clicked.connect(lambda: widgets.btnPauseTimer.setDisabled(True))
        widgets.btnPauseTimer.clicked.connect(lambda: widgets.btnResetTimer.setDisabled(False))
        widgets.btnResetTimer.clicked.connect(self.resetTimer)
        widgets.btnResetTimer.clicked.connect(lambda: widgets.btnStartTimer.setDisabled(False))
        widgets.btnResetTimer.clicked.connect(lambda: widgets.btnPauseTimer.setDisabled(True))
        widgets.btnResetTimer.clicked.connect(lambda: widgets.btnResetTimer.setDisabled(False))

        widgets.workMinutesSpinBox.valueChanged.connect(self.updateWorkValue)
        widgets.shortMinutesSpinBox.valueChanged.connect(self.updateShortRestValue)
        widgets.longMinutesSpinBox.valueChanged.connect(self.updateLongRestValue)

    def setupWidgets(self):
        widgets.tblTasks.horizontalHeader().setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
        widgets.tblTasks.horizontalHeader().setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)
        self.loadDataInTable()

        widgets.workMinutesSpinBox.setValue(int(self.settings.value(workMinutesKey, 25)))
        widgets.shortMinutesSpinBox.setValue(int(self.settings.value(shortMinutesKey, 5)))
        widgets.longMinutesSpinBox.setValue(int(self.settings.value(longMinutesKey, 15)))

        self.showNumPomodoros(0)

    # Pomodoro Timer Functions

    def updateCurrentMode(self, mode):
        if not self.allowChangeModeManually:
            msgBox = QtWidgets.QMessageBox(self)
            msgBox.setText("Pomodoro ainda em andamento...")
            msgBox.setInformativeText("Trocar de estado resetará o atual progresso")
            msgBox.setStandardButtons(QtWidgets.QMessageBox.Cancel | QtWidgets.QMessageBox.Apply)
            msgBox.setDefaultButton(QtWidgets.QMessageBox.Cancel)
            msgBox.show()
            ret = msgBox.exec()

            if ret == QtWidgets.QMessageBox.Cancel:
                self.allowChangeModeManually = False
                return
            else:
                self.allowChangeModeManually = True
                self.currentPomodoros = 1
        self.currentMode = mode
        self.resetTimer()

    def startTimer(self):
        if self.currentMode == Mode.work:
            widgets.btnPomodoro.click()
            self.allowChangeModeManually = False
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
        self.allowChangeModeManually = True
        self.purpleFile = "themes/pyjuco_purple.qss"
        self.blueFile = "themes/pyjuco_blue.qss"
        self.greenFile = "themes/pyjuco_green.qss"
        widgets.btnStartTimer.setDisabled(False)
        widgets.btnPauseTimer.setDisabled(True)
        widgets.btnResetTimer.setDisabled(False)
        self.workSecondPercent = 1/(int(self.settings.value(workMinutesKey, 25))*60/100)
        self.shortRestSecondPercent =  1/(int(self.settings.value(shortMinutesKey, 5))*60/100)
        self.longRestSecondPercent = 1/(int(self.settings.value(longMinutesKey, 15))*60/100)

        try:
            self.pauseTimer()
            if self.currentMode == Mode.work:
                self.time = self.workEndTime
            elif self.currentMode == Mode.short_rest:
                self.time = self.shortRestEndTime
            elif self.currentMode == Mode.long_rest:
                self.time = self.longRestEndTime
            else:
                pass
            self.displayTime()
            self.progressValue = 0
            widgets.progressBar.setValue(self.progressValue)
        except:
            pass

    def updateTime(self):
        self.time = self.time.addSecs(-30)
        self.totalTime = self.totalTime.addSecs(-1)
        if self.currentMode is Mode.work:
            self.workTime = self.workTime.addSecs(1)
            self.progressValue += self.workSecondPercent
        elif self.currentMode is Mode.short_rest:
            self.restTime = self.restTime.addSecs(1)
            self.progressValue += self.shortRestSecondPercent
        elif self.currentMode is Mode.long_rest:
            self.restTime = self.restTime.addSecs(1)
            self.progressValue += self.longRestSecondPercent
        else:
            pass 

        widgets.progressBar.setValue(self.progressValue)
        self.displayTime()

    def maybeChangeMode(self):
        print("="*50)
        print(f'current mode: {self.currentMode}\nself.time: {self.time}')
        print(f'change to long rest? {self.changeToLongRest()}')
        print(f'current pomodoros {self.currentPomodoros}')
        print(f'percentage of progress: {self.workSecondPercent} {self.shortRestSecondPercent} {self.longRestSecondPercent}')
        print("="*50)
        print(self.currentMode is Mode.work and self.time <= QtCore.QTime(0, 0, 0, 0))
        if self.currentMode is Mode.work and self.time <= QtCore.QTime(0, 0, 0, 0) and not self.changeToLongRest():
            self.showNumPomodoros(self.currentPomodoros)
            print("rest time!")
            self.currentMode = Mode.short_rest
            self.setButtonsEnabled()
            self.resetTimer()
            widgets.btnShortRest.click()
        elif self.currentMode is Mode.short_rest and self.time <= QtCore.QTime(0, 0, 0, 0) and not self.changeToLongRest():
            print("work time!")
            self.currentMode = Mode.work
            self.currentPomodoros += 1
            self.setButtonsEnabled()
            self.resetTimer()
            widgets.btnPomodoro.click()
        elif self.time <= QtCore.QTime(0, 0, 0, 0) and self.changeToLongRest():
            self.showNumPomodoros(self.currentPomodoros)
            print("long rest time")
            self.currentMode = Mode.long_rest
            self.currentPomodoros = 1
            self.setButtonsEnabled()
            self.resetTimer()
            widgets.btnLongRest.click()
        elif self.currentMode is Mode.long_rest and self.time <= QtCore.QTime(0, 0, 0, 0):
            self.showNumPomodoros(0)
            print("back to new pomodoro cycle!")
            self.currentMode = Mode.work
            self.resetTimer()
            widgets.btnPomodoro.click()
            self.setButtonsEnabled()
            
        else:
            pass

    def setButtonsEnabled(self):
        widgets.btnPauseTimer.setEnabled(False)
        widgets.btnResetTimer.setEnabled(False)
        widgets.btnStartTimer.setEnabled(True)

    def changeToLongRest(self):
        return self.currentPomodoros == self.maxPomodoros

    def showNumPomodoros(self, value):
        widgets.lblStudyCount.setText(f'Número de estudos: {value}')

    def displayTime(self):
        print(self.time.toString(self.timeFormat))
        widgets.lcdPomodoroTimer.display(self.time.toString(self.timeFormat))

    def showWindowMessage(self, status):
        if status is Status.workFinished:
            print('resting')
        elif status is Status.restFinished:
            print('work')
        else:
            print('finished')
            self.resetTimer()

    # Task Functions

    def loadDataInTable(self):
        widgets.tblTasks.clearContents()
        with DBMainOperations() as db:
            tasks = db.cursor.execute("SELECT * FROM tasks ORDER BY start_date").fetchall()
            widgets.tblTasks.setRowCount(len(tasks))
            topics = db.getAllRecords(tbl='topics')
            tasks = db.cursor.execute("SELECT * FROM tasks ORDER BY start_date").fetchall()
        try:
            tablerow = 0
            for row in tasks:
                widgets.tblTasks.setRowHeight(tablerow, 50)
                #startDate, endDate = self.formatDate(row[2], row[3])
                widgets.tblTasks.setItem(tablerow, 0, QtWidgets.QTableWidgetItem(row[0]))  #row[0] = task_name
                widgets.tblTasks.setItem(tablerow, 1, QtWidgets.QTableWidgetItem('self.topics[row[4]][1]')) #row[4] = topic_id
                tablerow += 1
            widgets.tblTasks.setRowHeight(tablerow, 50)
        except Exception:
            print('ERROR')

    def markTaskAsFinished(self, row):
        item = widgets.tblTasks.item(row, 0)
        font = widgets.tblTasks.item(row, 0).font()
        font.setStrikeOut(False if item.font().strikeOut() else True)
        item.setFont(font)
        with DBMainOperations() as db:
            qry = f"UPDATE tasks SET status = 'Finalizada' WHERE task_name = '{item.text()}'"
            db.cursor.execute(qry)

    def showTaskInLabel(self, row):
        widgets.lblActualTask.setText(widgets.tblTasks.item(row, 0).text())

    # Settings

    def updateMaxPomodoros(self):
        value = 3
        self.maxPomodoros = value

    def updateWorkValue(self):
        workNewValue = widgets.workMinutesSpinBox.value()
        self.settings.setValue(workMinutesKey, workNewValue)
        self.workEndTime = QtCore.QTime(0, workNewValue, 0)

    def updateShortRestValue(self):
        restNewValue = widgets.shortMinutesSpinBox.value()
        self.settings.setValue(shortMinutesKey, restNewValue)
        self.shortRestEndTime = QtCore.QTime(0, restNewValue, 0)

    def updateLongRestValue(self):
        restNewValue = widgets.longMinutesSpinBox.value()
        self.settings.setValue(longMinutesKey, restNewValue)
        self.longRestEndTime = QtCore.QTime(0, restNewValue, 0)
        
