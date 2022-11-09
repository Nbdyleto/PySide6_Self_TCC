from enum import Enum
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
    restFinished = 2
    repetitionsReached = 3

class NewPomodoroMainPage(QtWidgets.QWidget):
    def __init__(self):
        super(NewPomodoroMainPage, self).__init__()
        self.ui = Ui_Widget()
        self.ui.setupUi(self)
        self.setupVariables()
        self.setupConnections()
        self.setupTableResize()

        self.displayTime()

    def setupVariables(self):
        global widgets
        widgets = self.ui
        # QTime Variables
        self.settings = QtCore.QSettings()
        self.workEndTime = QtCore.QTime(
            int(self.settings.value(workHoursKey, 0)),
            int(self.settings.value(workMinutesKey, 0)),
            int(self.settings.value(workSecondsKey, 5)),
        )
        self.restEndTime = QtCore.QTime(
            int(self.settings.value(restHoursKey, 0)),
            int(self.settings.value(restMinutesKey, 0)),
            int(self.settings.value(restSecondsKey, 3)),
        )
        self.timeFormat = "hh:mm:ss"
        self.time = self.workEndTime
        self.workTime = QtCore.QTime(0, 0, 0, 0)
        self.restTime = QtCore.QTime(0, 0, 0, 0)
        self.totalTime = QtCore.QTime(0, 0, 0, 0)
        self.currentMode = Mode.work
        self.maxRepetitions = -1
        self.currentRepetitions = 0
        self.activeMode = "short_rest"
        # Progress Bar Variables
        self.workSecondPercent = 1/(25*60/100)
        self.restSecondPercent =  1/(5*60/100)
        self.progressValue = 0
    
    def setupConnections(self):
        widgets.btnStartTimer.clicked.connect(self.startTimer)
        widgets.btnResetTimer.clicked.connect(self.resetTimer)
        widgets.tblTasks.cellDoubleClicked.connect(self.markTaskAsFinished)
        widgets.tblTasks.cellClicked.connect(self.showTaskInLabel)

    def setupTableResize(self):
        widgets.tblTasks.horizontalHeader().setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
        widgets.tblTasks.horizontalHeader().setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)
        self.loadDataInTable()

    # Pomodoro Timer Functions

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
        self.currentMode = Mode.work if mode == "work" else Mode.short_rest

    def updateTime(self):
        self.time = self.time.addSecs(-1)
        self.totalTime = self.totalTime.addSecs(-1)
        if self.activeMode == "work":
            self.workTime = self.workTime.addSecs(1)
        else:
            self.restTime = self.restTime.addSecs(1)
        self.progressValue += self.workSecondPercent
        widgets.progressBar.setValue(self.progressValue)
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
            self.activeMode = "short_rest"
            self.incrementCurrentRepetitions()
            started = self.maybeStartTimer()
            self.showWindowMessage(Status.workFinished if started else Status.repetitionsReached)
        elif self.currentMode is Mode.short_rest and self.time >= self.restEndTime:
            self.resetTimer()
            self.activeMode = "work"
            self.incrementCurrentRepetitions()
            started = self.maybeStartTimer()
            self.showWindowMessage(Status.restFinished if started else Status.repetitionsReached)

    def incrementCurrentRepetitions(self):
        if self.maxRepetitions > 0:
            self.currentRepetitions += 1

    def displayTime(self):
        widgets.lcdPomodoroTimer.display(self.time.toString(self.timeFormat))

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
    """
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
    """