from functools import reduce
from PySide6 import QtCore, QtGui, QtWidgets
from functions.db_main_operations import DBMainOperations

from functions.new_daily_task.ui_daily_task import Ui_DailyTaskPage

class DTaskMainPage(QtWidgets.QWidget):
    def __init__(self):
        super(DTaskMainPage, self).__init__()
        self.ui = Ui_DailyTaskPage()
        self.ui.setupUi(self)
        self.setupVariables()
        self.setupConnections()
        self.setupWidgets()

    def setupVariables(self):
        # SET AS GLOBAL WIDGETS
        # ///////////////////////////////////////////////////////////////
        global widgets
        widgets = self.ui
        self.selectedTask, self.activeCalendar, self.activeTable = None, None, None

        self.filterByTopic, self.filterByStatus = False, False
        self.activeTopicId, self.activeStatus = None, None

    def setupConnections(self):
        widgets.tblTasks.cellClicked.connect(self.rowClickedFunctions)
        widgets.tblTasks.itemChanged.connect(self.updateDBRecord)
        widgets.tblLists.cellClicked.connect(self.updateStatusOrTopic)
        widgets.qCalendar.selectionChanged.connect(self.updateCalendarDate)
        widgets.btnOrderByTopic.clicked.connect(self.loadTopicsInList)
        widgets.btnOrderByStatus.clicked.connect(self.loadStatusInList)
        widgets.listByTopic.itemClicked.connect(self.checkTopicFilter)
        widgets.listByStatus.itemClicked.connect(self.checkStatusFilter)

    def setupWidgets(self):
        # tblTasks PARAMETERS
        # ///////////////////////////////////////////////////////////////
        widgets.tblTasks.setColumnWidth(0,350)
        widgets.tblTasks.horizontalHeader().setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)
        widgets.tblTasks.horizontalHeader().setSectionResizeMode(2, QtWidgets.QHeaderView.Stretch)
        widgets.tblTasks.horizontalHeader().setSectionResizeMode(3, QtWidgets.QHeaderView.Stretch)
        widgets.tblTasks.horizontalHeader().setSectionResizeMode(4, QtWidgets.QHeaderView.Stretch)
        widgets.tblTasks.horizontalHeader().setSectionResizeMode(5, QtWidgets.QHeaderView.Stretch)
        widgets.tblTasks.setStyleSheet("""
            QTableWidget::item{
                margin-top: 3px;          
                padding-left: 15px;
                text-align: center;
            }
        """)
        self.hideAll()

        widgets.tblLists.setVisible(False)
        widgets.tblLists.setColumnCount(1)
        widgets.tblLists.horizontalHeader().setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)

        widgets.btnOrderByTopic.clicked.connect(lambda: widgets.frameByTopic.setVisible(True))
        widgets.btnOrderByTopic.clicked.connect(lambda: widgets.btnOrderByTopic.setEnabled(False))
        widgets.btnOrderByStatus.clicked.connect(lambda: widgets.frameByStatus.setVisible(True))
        widgets.btnOrderByStatus.clicked.connect(lambda: widgets.btnOrderByStatus.setEnabled(False))

    # LOAD DATA FUNCTIONS
    # ///////////////////////////////////////////////////////////////

    def loadDataInTable(self):
        widgets.tblTasks.clearContents()
        qry = f"""SELECT * FROM TASKS"""    # Default
        showemptyrow = True
        ### FILTER OPTIONS
        if self.filterByTopic and not self.filterByStatus:
            print("FILTERING JUST BY TOPIC")
            qry = f"""SELECT * FROM TASKS
                      WHERE (topic_id = {self.activeTopicId})"""
        elif self.filterByStatus and not self.filterByTopic:
            print("FILTERING JUST BY STATUS")
            qry = f"""SELECT * FROM TASKS
                      WHERE (status = '{self.activeStatus}')"""
            showemptyrow = False
        elif self.filterByStatus and self.filterByTopic:
            print("FILTERING BY TOPIC AND BY STATUS")
            qry = f"""SELECT * FROM TASKS
                      WHERE (topic_id = {self.activeTopicId}) AND 
                            (status = '{self.activeStatus}')"""
            showemptyrow = False
        else:
            pass
        print(f'\nQUERY: {qry}')

        try:
            with DBMainOperations() as db:
                tasks = db.cursor.execute(qry).fetchall()
                print(f'{tasks}')
                rowcount = len(tasks)+1 if showemptyrow else len(tasks)
                widgets.tblTasks.setRowCount(rowcount)
            tablerow = 0
            for row in tasks:
                #print('\n', row)
                widgets.tblTasks.setRowHeight(tablerow, 50)
                taskid, taskname, status = row[0], row[1], row[2]
                startDate, endDate = self.formatDate(row[3], row[4])
                topic = self.getTopicName(row[5])
                btnRemoveTask = self.buttonToPutInRow(tablerow, taskid)
                widgets.tblTasks.setItem(tablerow, 0, QtWidgets.QTableWidgetItem(taskname))  #row[1] = task_name
                widgets.tblTasks.setItem(tablerow, 1, QtWidgets.QTableWidgetItem(status))  #row[2] = status
                widgets.tblTasks.setItem(tablerow, 2, QtWidgets.QTableWidgetItem(startDate)) #row[3] = start_date
                widgets.tblTasks.setItem(tablerow, 3, QtWidgets.QTableWidgetItem(endDate)) #row[4] = end_date
                widgets.tblTasks.setItem(tablerow, 4, QtWidgets.QTableWidgetItem(topic)) #row[5] = topic_id
                widgets.tblTasks.setCellWidget(tablerow, 5, btnRemoveTask)
                tablerow += 1 
            widgets.tblTasks.setRowHeight(tablerow, 50)
        except Exception as e:
            print('ERROR: ', e)

    def buttonToPutInRow(self, tablerow, taskid):
        btnRemoveTask = QtWidgets.QPushButton(widgets.tblTasks)
        btnRemoveTask.setMinimumSize(QtCore.QSize(0, 100))
        btnRemoveTask.setMaximumSize(QtCore.QSize(90, 16777215))
        btnRemoveTask.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        btnRemoveTask.setLayoutDirection(QtCore.Qt.LeftToRight)
        btnRemoveTask.setObjectName(f'btnRemoveTask{tablerow}')
        btnRemoveTask.setStyleSheet(u"""
            background-image: url(:/icons/images/icons/cil-x-circle.png);
            background-repeat: no-repeat;
            margin-top: 15px; 
            border-color: transparent;
        """)
        btnRemoveTask.clicked.connect(lambda: self.removeTask(taskid))
        return btnRemoveTask

    def removeTask(self, taskid):
        with DBMainOperations() as db:
            db.cursor.execute(f"DELETE from tasks WHERE task_id={taskid}")
        self.loadDataInTable()

    def getTopicName(self, topicid):
        with DBMainOperations() as db:
            name = db.getAllRecords(tbl='topics', whclause=f'topic_id = "{topicid}"')[0][1] # get topic_name
        return name

    def formatDate(self, startDate, endDate):
        x = startDate.split('-')
        formatedStartDate = QtCore.QDate(int(x[0]), int(x[1]), int(x[2])).toString(QtCore.Qt.RFC2822Date)
        y = endDate.split('-')
        formatedEndDate = QtCore.QDate(int(y[0]), int(y[1]), int(y[2])).toString(QtCore.Qt.RFC2822Date)
        return formatedStartDate, formatedEndDate
    
    # ROW CLICKED FUNCTIONS
    # ///////////////////////////////////////////////////////////////

    def rowClickedFunctions(self, row, col):
        if self.isExistentInDB(row):
            widgets.lblSetInfo.setVisible(True)
            if col == 1:
                self.loadStatusList()
            elif col == 2:
                self.showInitialDate()
            elif col == 3:
                self.showEndDate()
            elif col == 4:
                self.loadTopicsInTable()
            else: 
                self.hideAll()
        else:
            print('no correspondence in db!')

    def isExistentInDB(self, row):
        self.hideAll()
        with DBMainOperations() as db:
            try:
                taskname = widgets.tblTasks.item(row, 0).text()
                self.selectedTask = db.getAllRecords(tbl='tasks', specifcols='task_name', 
                                                     whclause=f'task_name = "{taskname}"')[0][0]
                print(self.selectedTask)
                return True
            except Exception:
                self.selectedTask = ''
                return False

    def hideAll(self):
        self.activeTable = None
        widgets.tblLists.clearContents()
        widgets.qCalendar.clearMask()
        widgets.lblSetInfo.setVisible(False)
        widgets.qCalendar.setVisible(False)
        widgets.tblLists.setVisible(False)
        widgets.lblSetInfo.setVisible(False)

    def loadStatusList(self):
        self.activeTable = 'tblStatus'
        widgets.lblSetInfo.setText('Status:')
        widgets.tblLists.show()
        widgets.tblLists.setObjectName('tblStatus')
        widgets.tblLists.setRowCount(3)
        widgets.tblLists.setItem(0, 0, QtWidgets.QTableWidgetItem('Não Iniciada.'))
        widgets.tblLists.setItem(1, 0, QtWidgets.QTableWidgetItem('Em Progresso...'))
        widgets.tblLists.setItem(2, 0, QtWidgets.QTableWidgetItem('Finalizada!'))
    
    def loadTopicsInTable(self):
        self.activeTable = 'tblTopics'
        widgets.tblLists.show()
        widgets.tblLists.setObjectName('tblTopics')
        widgets.lblSetInfo.setText('Tópico:')
        with DBMainOperations() as db:
            topicscount = db.cursor.execute("SELECT COUNT(*) FROM topics").fetchone()[0]
            widgets.tblLists.setRowCount(topicscount+1)
            topics = db.getAllRecords(tbl='topics')
            print(f'topics: {topics}')
        tablerow = 0
        for row in topics:
            widgets.tblLists.setItem(tablerow, 0, QtWidgets.QTableWidgetItem(row[1]))
            tablerow += 1
        lastrow = len(topics)
        widgets.tblLists.setItem(lastrow, 0, QtWidgets.QTableWidgetItem('Inserir novo tópico...'))

    def showInitialDate(self):
        self.activeCalendar = 'calInitialDate'
        widgets.qCalendar.setObjectName('calInitialDate')
        widgets.qCalendar.show()
        widgets.lblSetInfo.setText('Data Inicial:')

    def showEndDate(self):
        self.activeCalendar = 'calEndDate'
        widgets.qCalendar.setObjectName('calEndDate')
        widgets.qCalendar.show()
        widgets.lblSetInfo.setText('Data Final:')

    # UPDATE IN DB FUNCTIONS
    # ///////////////////////////////////////////////////////////////

    def updateDBRecord(self, item):
        if self.selectedTask == '':
            # Not existent in db, so, create new data.
            with DBMainOperations() as db:
                qry = 'SELECT * FROM tasks ORDER BY task_id DESC LIMIT 1;'
                lastid = db.cursor.execute(qry).fetchall()[0][0]+1
                sysdate = QtCore.QDate.currentDate().toString(QtCore.Qt.ISODate)
                newdata = (lastid, item.text(), "Não Iniciada.", sysdate, sysdate, 0)
                db.populateTbl('tasks', params=newdata)
            print('adding...')
        elif self.selectedTask is not None:
            # Existent in db, so, update old data.
            oldtask = self.selectedTask
            with DBMainOperations() as db:
                db.cursor.execute(f"UPDATE tasks SET task_name = '{item.text()}' WHERE task_name = '{oldtask}'")
            print('changing...')
        else:
            return
        self.selectedTask = None
        self.loadDataInTable()

    def updateStatusOrTopic(self, row):
        # verify if clicked row is the last row.
        print(f'row: {row} and rowcount: {widgets.tblLists.rowCount()}')
        if row == widgets.tblLists.rowCount()-1 and self.activeTable == 'tblTopics':
            # Add new topic.
            print('last row!')
            self.addNewTopic()
            self.activeTable == 'tblTopics'
        else:
            # Update topic.
            if self.activeTable == 'tblStatus':
                with DBMainOperations() as db:
                    newstatus = widgets.tblLists.item(row, 0).text()
                    db.cursor.execute(f"UPDATE tasks SET status = '{newstatus}' WHERE task_name = '{self.selectedTask}'")
            elif self.activeTable == 'tblTopics':
                topicname = widgets.tblLists.item(row, 0).text()
                with DBMainOperations() as db:
                    newid = db.getAllRecords(tbl='topics', whclause=f'topic_name = "{topicname}"')[0][0] # get topic_id
                    db.cursor.execute(f"UPDATE tasks SET topic_id = '{newid}' WHERE task_name = '{self.selectedTask}'")
            else:
                return
            self.selectedTask, self.activeTable = None, None
            self.loadDataInTable()
            self.hideAll()

    def addNewTopic(self):
        newtopic, inputstatus = QtWidgets.QInputDialog.getText(
            self, "Novo Tópico", "Entre com o nome do novo tópico:")
        with DBMainOperations() as db:
            if inputstatus:
                qry = 'SELECT * FROM topics ORDER BY topic_id DESC LIMIT 1;'
                lastid = db.cursor.execute(qry).fetchall()[0][0]+1
                print('lastid:', lastid)
                db.populateTbl(tbl='topics', params=(lastid, newtopic))
        self.hideAll()
        self.loadTopicsInTable()
        #self.loadDataInTable()

    def updateCalendarDate(self):
        newdate = widgets.qCalendar.selectedDate().toString(QtCore.Qt.ISODate)
        print(newdate)
        if self.activeCalendar == 'calInitialDate':
            with DBMainOperations() as db: 
                db.cursor.execute(f"UPDATE tasks SET start_date = '{newdate}' WHERE task_name = '{self.selectedTask}'")
        elif self.activeCalendar == 'calEndDate':
            with DBMainOperations() as db: 
                db.cursor.execute(f"UPDATE tasks SET end_date = '{newdate}' WHERE task_name = '{self.selectedTask}'")
        self.selectedTask, self.activeCalendar = None, None
        self.loadDataInTable()
        self.hideAll()

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