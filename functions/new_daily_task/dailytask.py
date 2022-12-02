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
        self.activeTopicID, self.activeStatus = 0, None

    def setupConnections(self):
        widgets.tblTasks.cellClicked.connect(self.rowClickedFunctions)
        widgets.tblTasks.doubleClicked.connect(self.addTask)
        widgets.tblLists.cellClicked.connect(self.updateStatusOrTopic)
        widgets.qCalendar.selectionChanged.connect(self.updateCalendarDate)
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
        widgets.tblTasks.horizontalHeader().setSectionResizeMode(6, QtWidgets.QHeaderView.Stretch)
        widgets.tblTasks.setStyleSheet("""
            QTableWidget::item{
                margin-top: 3px;          
                padding-left: 15px;
                text-align: center;
            }
        """)
        
        self.hideAll()
        self.loadTopicsInList()
        self.loadStatusInList()

        widgets.tblLists.setVisible(False)
        widgets.tblLists.setColumnCount(1)


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
                      WHERE (topic_id = {self.activeTopicID})"""
        elif self.filterByStatus and not self.filterByTopic:
            print("FILTERING JUST BY STATUS")
            qry = f"""SELECT * FROM TASKS
                      WHERE (status = '{self.activeStatus}')"""
            showemptyrow = False
        elif self.filterByStatus and self.filterByTopic:
            print("FILTERING BY TOPIC AND BY STATUS")
            qry = f"""SELECT * FROM TASKS
                      WHERE (topic_id = {self.activeTopicID}) AND 
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
                btnRemoveTask, btnEditTask = self.buttonToPutInRow(tablerow, taskid)
                widgets.tblTasks.setItem(tablerow, 0, QtWidgets.QTableWidgetItem(taskname))  #row[1] = task_name
                widgets.tblTasks.setItem(tablerow, 1, QtWidgets.QTableWidgetItem(status))  #row[2] = status
                widgets.tblTasks.setItem(tablerow, 2, QtWidgets.QTableWidgetItem(startDate)) #row[3] = start_date
                widgets.tblTasks.setItem(tablerow, 3, QtWidgets.QTableWidgetItem(endDate)) #row[4] = end_date
                widgets.tblTasks.setItem(tablerow, 4, QtWidgets.QTableWidgetItem(topic)) #row[5] = topic_id
                widgets.tblTasks.setCellWidget(tablerow, 5, btnEditTask)
                widgets.tblTasks.setCellWidget(tablerow, 6, btnRemoveTask)
                # Set bold if is a ended task:
                for col in range(5):
                    item = widgets.tblTasks.item(tablerow, col)
                    font = widgets.tblTasks.item(tablerow, col).font()
                    font.setBold(True if status == 'Finalizada!' else False)
                    item.setFont(font)

                tablerow += 1 
            widgets.tblTasks.setRowHeight(tablerow, 50)
            ## SET LAST ROW VALUES:
            lastrow = len(tasks)
            widgets.tblTasks.setItem(lastrow, 0, QtWidgets.QTableWidgetItem('Duplo clique para inserir...'))
            widgets.tblTasks.setCellWidget(tablerow, 5, QtWidgets.QWidget())
            widgets.tblTasks.setCellWidget(tablerow, 6, QtWidgets.QWidget())
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

        btnEditTask = QtWidgets.QPushButton(widgets.tblTasks)
        btnEditTask.setMinimumSize(QtCore.QSize(40, 100))
        btnEditTask.setMaximumSize(QtCore.QSize(90, 16777215))
        btnEditTask.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        btnEditTask.setLayoutDirection(QtCore.Qt.LeftToRight)
        btnEditTask.setObjectName(f'btnEditTask{tablerow}')
        btnEditTask.setStyleSheet(u"""
        QPushButton{
            background-image: url(:/icons/images/icons/cil-pencil.png);
            background-repeat: no-repeat;
            margin-top: 15px; 
            border-color: transparent;
            }
        QToolTip{background-image: none;}
        """)
        btnEditTask.setToolTip('Editar deck')
        btnEditTask.clicked.connect(lambda: self.editTaskName(taskid))
        return btnRemoveTask, btnEditTask

    def removeTask(self, taskid):
        with DBMainOperations() as db:
            db.cursor.execute(f"DELETE from tasks WHERE task_id={taskid}")
        self.loadDataInTable()

    def editTaskName(self, taskid):
        with DBMainOperations() as db:
            taskname = db.getAllRecords(tbl='tasks', specifcols='task_name', whclause=f'task_id == {taskid}')[0][0]
            newvalue, inputstatus = QtWidgets.QInputDialog.getText(self, "Alterar Nome da Tarefa", f"{taskname}")
            if inputstatus:
                db.cursor.execute(f"UPDATE tasks SET task_name = '{newvalue}' WHERE task_id == {taskid}")
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
                self.loadStatusInTable()
            elif col == 2:
                self.showInitialDate()
            elif col == 3:
                self.showEndDate()
            elif col == 4:
                self.loadTopicsInTable()
            else: 
                self.hideAll()
        else:
            print(f'{row} no correspondence in db!')

    def addTask(self, item):
        print("ROW CLICADA: ", item.row())
        if not self.isExistentInDB(item.row()):    # last row
            with DBMainOperations() as db:
                newvalue, inputstatus = QtWidgets.QInputDialog.getText(self, "Adicionar tarefa", "Adicione o nome da tarefa. Cuidaremos do resto!")
                if inputstatus:
                    qry = 'SELECT * FROM tasks ORDER BY task_id DESC LIMIT 1;'
                    lastid = db.cursor.execute(qry).fetchall()[0][0]+1
                    sysdate = QtCore.QDate.currentDate().toString(QtCore.Qt.ISODate)
                    topicid = (self.activeTopicID if self.activeTopicID != -1 else 0)
                    newdata = (lastid, newvalue, "Não Iniciada.", sysdate, sysdate, topicid)
                    db.populateTbl('tasks', params=newdata)
                    self.loadDataInTable()

    def isExistentInDB(self, row):
        self.hideAll()
        with DBMainOperations() as db:
            try:
                taskname = widgets.tblTasks.item(row, 0).text()
                self.selectedTask = db.getAllRecords(tbl='tasks', specifcols='task_name', 
                                                     whclause=f'task_name = "{taskname}"')[0][0]
                print("EXIST!")
                print('task: ', self.selectedTask)
                return True
            except Exception:
                self.selectedTask = ''
                print("NOT EXIST!")
                return False

    def hideAll(self):
        self.activeTable = None
        widgets.tblLists.setColumnCount(0)
        widgets.tblLists.clearContents()
        widgets.qCalendar.clearMask()
        widgets.lblSetInfo.setVisible(False)
        widgets.qCalendar.setVisible(False)
        widgets.tblLists.setVisible(False)
        widgets.lblSetInfo.setVisible(False)

    def loadStatusInTable(self):
        self.activeTable = 'tblStatus'
        widgets.tblLists.setColumnCount(1)
        widgets.tblLists.horizontalHeader().setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
        widgets.tblLists.setColumnWidth(1,20)
        widgets.lblSetInfo.setText('Status:')
        widgets.tblLists.show()
        widgets.tblLists.setObjectName('tblStatus')
        widgets.tblLists.setRowCount(3)
        widgets.tblLists.setItem(0, 0, QtWidgets.QTableWidgetItem('Não Iniciada.'))
        widgets.tblLists.setItem(1, 0, QtWidgets.QTableWidgetItem('Em Progresso...'))
        widgets.tblLists.setItem(2, 0, QtWidgets.QTableWidgetItem('Finalizada!'))
    
    def loadTopicsInTable(self):
        widgets.tblLists.setColumnCount(2)
        widgets.tblLists.horizontalHeader().setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
        widgets.tblLists.setColumnWidth(1,60)
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
        lastrow = len(topics)
        for row in topics:
            widgets.tblLists.setItem(tablerow, 0, QtWidgets.QTableWidgetItem(row[1]))
            if tablerow > 0:    # add remove topic button after row 0
                topicid = row[0]
                btnRemoveTopic = self.buttonToPutInTopicsRow(tablerow=tablerow, topicid=topicid)
                widgets.tblLists.setCellWidget(tablerow, 1, btnRemoveTopic)
            tablerow += 1
        widgets.tblLists.setItem(lastrow, 0, QtWidgets.QTableWidgetItem('Inserir novo tópico...'))
        widgets.tblLists.setCellWidget(tablerow, 1, QtWidgets.QWidget())

    def buttonToPutInTopicsRow(self, tablerow, topicid):
        btnRemoveTopic = QtWidgets.QPushButton(widgets.tblLists)
        btnRemoveTopic.setMinimumSize(QtCore.QSize(0, 100))
        btnRemoveTopic.setMaximumSize(QtCore.QSize(90, 16777215))
        btnRemoveTopic.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        btnRemoveTopic.setLayoutDirection(QtCore.Qt.LeftToRight)
        btnRemoveTopic.setObjectName(f'btnRemoveTopic{tablerow}')
        btnRemoveTopic.setStyleSheet(u"""
            background-image: url(:/icons/images/icons/cil-x-circle.png);
            background-repeat: no-repeat;
            margin-top: 3px; 
            border-color: transparent;
        """)
        btnRemoveTopic.clicked.connect(lambda: self.removeTopic(topicid=topicid))
        return btnRemoveTopic

    def removeTopic(self, topicid):
        msgBox = QtWidgets.QMessageBox(self)
        msgBox.setWindowTitle(f"Apagar {topicid}")
        msgBox.setText("Tem plena convicção disso?")
        msgBox.setStyleSheet('font: 15px;')
        msgBox.setInformativeText("Apagar um tópico também apagará as tarefas, flashcards e progresso associados a esse tópico.")
        msgBox.setStandardButtons(QtWidgets.QMessageBox.Cancel | QtWidgets.QMessageBox.Apply)
        msgBox.setDefaultButton(QtWidgets.QMessageBox.Cancel)
        msgBox.show()
        ret = msgBox.exec()

        if ret == QtWidgets.QMessageBox.Cancel:
            return
        else:
            with DBMainOperations() as db:
                db.cursor.execute(f"DELETE FROM topics WHERE topic_id={topicid}")
                db.cursor.execute(f"DELETE FROM tasks WHERE topic_id={topicid}")
                db.cursor.execute(f"DELETE FROM decks WHERE topic_id={topicid}")
                db.cursor.execute(f"DELETE FROM pomodoroProgress WHERE topic_id={topicid}")
            self.filterByTopic, self.filterByStatus = False, False
            self.loadTopicsInTable()
            self.loadTopicsInList()
            self.loadDataInTable()

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
            print('Not existent in db, so, create new data.')
            # Not existent in db, so, create new data.
            with DBMainOperations() as db:
                qry = 'SELECT * FROM tasks ORDER BY task_id DESC LIMIT 1;'
                lastid = db.cursor.execute(qry).fetchall()[0][0]+1
                sysdate = QtCore.QDate.currentDate().toString(QtCore.Qt.ISODate)
                topicid = (self.activeTopicID if self.activeTopicID != -1 else 0)
                newdata = (lastid, item.text(), "Não Iniciada.", sysdate, sysdate, topicid)
                db.populateTbl('tasks', params=newdata)
            print('adding...')
        elif self.selectedTask is not None:
            print('Existent in db, so, update old data.')
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
                self.loadTopicsInList()
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
        widgets.listByTopic.setCurrentItem(item)
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
            self.activeTopicID = -1
        elif item.text() == 'Sem tópico':
            self.filterByTopic = True
            self.activeTopicID = 0
        else:
            with DBMainOperations() as db:
                self.filterByTopic = True
                self.activeTopicID = db.getAllRecords(tbl='topics', specifcols='topic_id', whclause=f'topic_name = "{item.text()}"')[0][0]
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