from enum import Enum
from modules.app_functions import AppFunctions
from modules.app_settings import Settings
from playsound import playsound
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
        self.currentPomodoros = 0
        self.maxPomodoros = 3
        # Progress Bar Variables
        self.workSecondPercent = 1/(int(self.settings.value(workMinutesKey, 25))*60/100)
        self.shortRestSecondPercent =  1/(int(self.settings.value(shortMinutesKey, 5))*60/100)
        self.longRestSecondPercent = 1/(int(self.settings.value(longMinutesKey, 15))*60/100)
        self.progressValue = 0
        # Pallete Variables
        self.allowChangeModeManually = True
        # Filter Variables
        self.filterByTopic, self.filterByDate = False, False
        self.activeTopicId, self.activeDate = None, None
        # Progress Variables
        self.activeTaskTopicID = 0
        self.activePomodoroID = -1
        # Settings Variables
        self.autoPause = self.settings.value(autoPauseKey, defaultValue='No')
        self.autoPomo = self.settings.value(autoPomoKey, defaultValue='No')
        self.activeAlarm = self.settings.value(alarmKey, defaultValue='Actived')
        print('testing setttings 1:')
        print(f'auto pomo? {self.autoPomo}, auto pause? {self.autoPause}, alarm active? {self.activeAlarm}')

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

        widgets.listByTopic.itemClicked.connect(self.checkTopicFilter)

        widgets.btnSaveSettings.clicked.connect(self.updateSettings)

    def setupWidgets(self):
        widgets.tblTasks.horizontalHeader().setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
        widgets.tblTasks.horizontalHeader().setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)
        self.loadDataInTable()

        widgets.workMinutesSpinBox.setValue(int(self.settings.value(workMinutesKey, 25)))
        widgets.shortMinutesSpinBox.setValue(int(self.settings.value(shortMinutesKey, 5)))
        widgets.longMinutesSpinBox.setValue(int(self.settings.value(longMinutesKey, 15)))

        self.showNumPomodoros(0)
        print('testing setttings 2:')
        print(f'auto pomo? {self.autoPomo}, auto pause? {self.autoPause}, alarm active? {self.activeAlarm}')
        self.loadTopicsInList()
        if self.autoPause == 'Yes':
            widgets.rdbtnYesPauseAuto.setChecked(True)
            widgets.rdbtnNoPauseAuto.setChecked(False)
        else:
            widgets.rdbtnYesPauseAuto.setChecked(False)
            widgets.rdbtnNoPauseAuto.setChecked(True)
        if self.autoPomo == 'Yes':
            widgets.rdbtnYesPomoAuto.setChecked(True)
            widgets.rdbtnNoPomoAuto.setChecked(False)
        else: 
            widgets.rdbtnYesPomoAuto.setChecked(False)
            widgets.rdbtnNoPomoAuto.setChecked(True)
        if self.activeAlarm == 'Actived':
            widgets.rdbtnActivedAlarm.setChecked(True)
            widgets.rdbtnDeactivedAlarm.setChecked(False)
        else:
            widgets.rdbtnActivedAlarm.setChecked(False)
            widgets.rdbtnDeactivedAlarm.setChecked(True)

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

    def updateSettings(self):
        msgBox = QtWidgets.QMessageBox(self)
        msgBox.setText("Configurações aplicadas!")
        msgBox.setInformativeText("As configurações estarão ativas a partir do próximo estudo!")
        msgBox.show()
        print('ALEGRIAA')
        if widgets.rdbtnYesPomoAuto.isChecked():
            self.settings.setValue(autoPomoKey, 'Yes')
        else:
            self.settings.setValue(autoPomoKey, 'No')

        if widgets.rdbtnYesPauseAuto.isChecked():
            self.settings.setValue(autoPauseKey, 'Yes')
        else:
            self.settings.setValue(autoPauseKey, 'No')

        if widgets.rdbtnActivedAlarm.isChecked():
            self.settings.setValue(alarmKey, 'Actived')
        else:
            self.settings.setValue(alarmKey, 'Deactived')

        self.autoPause = self.settings.value(autoPauseKey, defaultValue='No')
        self.autoPomo = self.settings.value(autoPomoKey, defaultValue='No')
        self.activeAlarm = self.settings.value(alarmKey, defaultValue='Actived')

        print('new pause: ', self.settings.value(autoPauseKey))
        print('new pomo: ', self.settings.value(autoPomoKey))
        print('new alarm: ', self.settings.value(alarmKey))
        

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
                self.currentPomodoros = 0
                self.showNumPomodoros(self.currentPomodoros)
        self.currentMode = mode
        self.resetTimer()

    def startTimer(self):
        self.allowChangeModeManually = False
        if self.currentMode == Mode.work:
            self.createPomodoroInDB()
        try:
            if not self.timer.isActive():
                self.createTimer()
        except:
            self.createTimer()

    def createPomodoroInDB(self):
        with DBMainOperations() as db:
            try:
                qry = 'SELECT * FROM topics ORDER BY pomo_id DESC LIMIT 1;'
                lastid = db.cursor.execute(qry).fetchall()[0][0]+1
            except:
                lastid = 0
            self.activePomodoroID = lastid
            studydate = QtCore.QDate.currentDate().toString(QtCore.Qt.ISODate)
            params = (self.activePomodoroID, False, studydate, QtCore.QTime(0, 0, 0).toString(), self.activeTaskTopicID)
            db.populateTbl(tbl='pomodoroProgress', params=params)
            toprint = db.getAllRecords(tbl='pomodoroProgress')
            print('pomo adicionado:', toprint)

    def updateTimeInDB(self):
        with DBMainOperations() as db:
            qry = f"UPDATE pomodoroProgress SET total_time = '{self.workTime}' WHERE pomo_id = {self.activePomodoroID};" 
            db.cursor.execute(qry)
            print('UPDATING...\n', db.getAllRecords(tbl='pomodoroProgress'))

    def setCompletedInDB(self):
        with DBMainOperations() as db:
            qry = f"UPDATE pomodoroProgress SET completed = True WHERE pomo_id = {self.activePomodoroID};"
            db.cursor.execute(qry)

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
            print('not enable reset!')

    def updateTime(self):
        self.time = self.time.addSecs(-30)
        self.totalTime = self.totalTime.addSecs(-1)
        self.updateTimeInDB()
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
            if self.activeAlarm == 'Actived':
                playsound('././sounds/forest-birds.wav')
            self.currentPomodoros += 1
            self.setCompletedInDB()
            self.showNumPomodoros(self.currentPomodoros)
            print("rest time, change to long rest? ", self.changeToLongRest())
            if not self.changeToLongRest():
                self.currentMode = Mode.short_rest
                self.setButtonsEnabled()
                self.resetTimer()
                widgets.btnLongRest.setDisabled(True)
                widgets.btnShortRest.click()
            else:
                msgBox = QtWidgets.QMessageBox(self)
                msgBox.setText("Ciclo de estudo finalizado!")
                msgBox.setInformativeText("Inicie o descanso longo")
                msgBox.show()
                self.currentMode = Mode.long_rest
                self.setButtonsEnabled()
                self.resetTimer()
                widgets.btnLongRest.setDisabled(False)
                widgets.btnLongRest.click()
            if self.autoPause == 'true':
                self.startTimer()

        elif self.currentMode is Mode.short_rest and self.time <= QtCore.QTime(0, 0, 0, 0) and not self.changeToLongRest():
            self.showNumPomodoros(self.currentPomodoros)
            print("work time!")
            self.currentMode = Mode.work
            self.setButtonsEnabled()
            self.resetTimer()
            widgets.btnLongRest.setDisabled(True)
            widgets.btnPomodoro.click()
            if self.autoPomo == 'true':
                self.startTimer()
        elif self.currentMode is Mode.long_rest and self.time <= QtCore.QTime(0, 0, 0, 0):
            self.showNumPomodoros(0)
            print("back to new pomodoro cycle!")
            self.currentMode = Mode.work
            self.currentPomodoros = 0
            self.resetTimer()
            widgets.btnLongRest.setDisabled(True)
            widgets.btnPomodoro.click()
            self.setButtonsEnabled()
            
        else:
            pass


    def setButtonsEnabled(self):
        widgets.btnPauseTimer.setEnabled(False)
        widgets.btnResetTimer.setEnabled(False)
        widgets.btnStartTimer.setEnabled(True)

    def changeToLongRest(self):
        return self.currentPomodoros >= self.maxPomodoros

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
        qry = f"""SELECT * FROM TASKS WHERE (status != 'Finalizada!')"""    # Default
        ### FILTER OPTIONS
        if self.filterByTopic and not self.filterByDate:
            print("FILTERING JUST BY TOPIC")
            qry = f"""SELECT * FROM TASKS
                      WHERE (topic_id = {self.activeTopicId}) AND 
                            (status != 'Finalizada!')"""
        elif self.filterByDate and not self.filterByTopic:
            print("FILTERING JUST BY DATE")
            qry = f"""SELECT * FROM TASKS
                      WHERE (end_date = '{self.activeEndDate}' AND 
                            (status != 'Finalizada!'))"""
        elif self.filterByDate and self.filterByTopic:
            print("FILTERING BY DATE AND BY TOPIC")
            qry = f"""SELECT * FROM TASKS
                      WHERE (topic_id = {self.activeTopicId}) AND 
                            (end_date = '{self.activeEndDate}') AND
                            (status != 'Finalizada!'))"""
        else:
            pass
        print(f'\nQUERY: {qry}')

        try:
            with DBMainOperations() as db:
                tasks = db.cursor.execute(qry).fetchall()
                print(f'{tasks}')
                widgets.tblTasks.setRowCount(len(tasks))
            tablerow = 0
            for row in tasks:
                #print('\n', row)
                widgets.tblTasks.setRowHeight(tablerow, 50)
                taskid, taskname = row[0], row[1]
                topic = self.getTopicName(row[5])
                widgets.tblTasks.setItem(tablerow, 0, QtWidgets.QTableWidgetItem(taskname))
                widgets.tblTasks.setItem(tablerow, 1, QtWidgets.QTableWidgetItem(topic))
                tablerow += 1 
            widgets.tblTasks.setRowHeight(tablerow, 50)
        except Exception as e:
            print('ERROR: ', e)

    def getTopicName(self, topicid):
        with DBMainOperations() as db:
            name = db.getAllRecords(tbl='topics', whclause=f'topic_id = "{topicid}"')[0][1] # get topic_name
        return name
    
    # ORDER BY FUNCTIONS
    # ///////////////////////////////////////////////////////////////

    def loadTopicsInList(self):
        widgets.listByTopic.clear()
        item = QtWidgets.QListWidgetItem()
        item.setText('Geral')
        widgets.listByTopic.addItem(item)
        with DBMainOperations() as db:
            topics = db.getAllRecords(tbl='topics', specifcols='topic_name')
        for topic in topics:
            item = QtWidgets.QListWidgetItem()
            item.setText(topic[0])
            if topic[0] == '':
                item.setText('Sem tópico')
            #qradiobtn = QtWidgets.QRadioButton(f'{topic}')
            #widgets.listByTopic.setItemWidget(item, qradiobtn)
            widgets.listByTopic.addItem(item)
    
    def checkTopicFilter(self, item):
        if item.text() == 'Geral':
            self.filterByTopic = False
            self.activeTopicId = -1
        elif item.text() == 'Sem tópico':
            self.filterByTopic = True
            self.activeTopicId = 0
        else:
            with DBMainOperations() as db:
                self.filterByTopic = True
                self.activeTopicId = db.getAllRecords(tbl='topics', specifcols='topic_id', whclause=f'topic_name = "{item.text()}"')[0][0]
        self.loadDataInTable()
    
    def loadStatusInList(self):
        widgets.listByStatus.clear()
        statuslist = ['Geral', 'Não Iniciada.', 'Em Progresso...', 'Finalizada!']
        for status in statuslist:
            item = QtWidgets.QListWidgetItem()
            item.setText(status)
            widgets.listByStatus.addItem(item)

    def checkStatusFilter(self, item):
        statuslist = ['Geral', 'Não Iniciada.', 'Em Progresso...', 'Finalizada!']
        self.filterByStatus = True
        if item.text() == statuslist[0]:
            self.activeStatus = None
            self.filterByStatus = False
        elif item.text() == statuslist[1]:
            self.activeStatus = statuslist[1]
        elif item.text() == statuslist[2]:
            self.activeStatus = statuslist[2]
        elif item.text() == statuslist[3]:
            self.activeStatus = statuslist[3]
        else: pass
        
        self.loadDataInTable()

    def markTaskAsFinished(self, row):
        item = widgets.tblTasks.item(row, 0)
        font = widgets.tblTasks.item(row, 0).font()
        font.setStrikeOut(False if item.font().strikeOut() else True)
        item.setFont(font)
        with DBMainOperations() as db:
            qry = f"UPDATE tasks SET status = 'Finalizada!' WHERE task_name = '{item.text()}'"
            db.cursor.execute(qry)

    def showTaskInLabel(self, row):
        taskname = widgets.tblTasks.item(row, 0).text()
        topicname = widgets.tblTasks.item(row, 1).text()
        widgets.lblActualTask.setText(f'{taskname} : {topicname}')
        with DBMainOperations() as db:
            topicid = db.getAllRecords(tbl='topics', specifcols='topic_id', 
                                        whclause=f'topic_name = "{topicname}"')[0][0]            
        self.activeTaskTopicID = topicid