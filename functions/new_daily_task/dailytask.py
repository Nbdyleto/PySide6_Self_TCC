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

        self.orderByState = False
        self.orderByTopics = []

    def setupConnections(self):
        widgets.tblTasks.cellClicked.connect(self.rowClickedFunctions)
        widgets.tblTasks.itemChanged.connect(self.updateDBRecord)
        widgets.tblLists.cellClicked.connect(self.updateStatusOrTopic)
        widgets.qCalendar.selectionChanged.connect(self.updateCalendarDate)
        widgets.btnOrderByTopic.clicked.connect(self.loadTopicsInList)
        
        widgets.listByTopic.itemChanged.connect(self.testCheck)

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
        widgets.btnOrderByTopic.clicked.connect(lambda: widgets.frameByStatus.setVisible(False))
        widgets.btnOrderByTopic.clicked.connect(lambda: widgets.frameByData.setVisible(False))
        widgets.btnOrderByStatus.clicked.connect(lambda: widgets.frameByTopic.setVisible(False))
        widgets.btnOrderByStatus.clicked.connect(lambda: widgets.frameByStatus.setVisible(True))
        widgets.btnOrderByStatus.clicked.connect(lambda: widgets.frameByData.setVisible(False))
        widgets.btnOrderByDate.clicked.connect(lambda: widgets.frameByTopic.setVisible(False))
        widgets.btnOrderByDate.clicked.connect(lambda: widgets.frameByStatus.setVisible(False))
        widgets.btnOrderByDate.clicked.connect(lambda: widgets.frameByData.setVisible(True))
    # LOAD DATA FUNCTIONS
    # ///////////////////////////////////////////////////////////////

    def loadDataInTable(self, orderByTopic=False, topics=None):
        widgets.tblTasks.clearContents()
        with DBMainOperations() as db:
            
            if orderByTopic:
                qry = "SELECT * FROM tasks WHERE (topic_id=?) ORDER BY start_date"
                _tasks = []
                taskscount = 0
                for topicid in topics:
                    _tasks.append(db.cursor.execute(qry, (topicid,)).fetchall())
                    taskscount += db.getAllRecords(tbl='tasks', specifcols='COUNT(*)', whclause=f'topic_id={topicid}')[0][0]
                widgets.tblTasks.setRowCount(taskscount)
                tasks = reduce(lambda a, b: a+b, _tasks) # Merge all tasks.
            else:
                qry = "SELECT * FROM tasks ORDER BY start_date"
                taskscount = db.cursor.execute("SELECT COUNT(*) FROM tasks").fetchone()[0]
                widgets.tblTasks.setRowCount(taskscount+1)
                tasks = db.cursor.execute(qry).fetchall()
        try:
            tablerow = 0
            for row in tasks:
                widgets.tblTasks.setRowHeight(tablerow, 50)
                startDate, endDate = self.formatDate(row[2], row[3])
                topic = self.getTopicName(row[4])
                widgets.tblTasks.setItem(tablerow, 0, QtWidgets.QTableWidgetItem(row[0]))  #row[0] = task_name
                widgets.tblTasks.setItem(tablerow, 1, QtWidgets.QTableWidgetItem(row[1]))  #row[1] = status
                widgets.tblTasks.setItem(tablerow, 2, QtWidgets.QTableWidgetItem(startDate)) #row[2] = start_date
                widgets.tblTasks.setItem(tablerow, 3, QtWidgets.QTableWidgetItem(endDate)) #row[3] = end_date
                widgets.tblTasks.setItem(tablerow, 4, QtWidgets.QTableWidgetItem(topic)) #row[4] = topic_id
                tablerow += 1
                
            widgets.tblTasks.setRowHeight(tablerow, 50)
        except Exception:
            print('ERROR')

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
                self.loadTopicsList()
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
        widgets.tblLists.setItem(0, 0, QtWidgets.QTableWidgetItem('Não iniciada.'))
        widgets.tblLists.setItem(1, 0, QtWidgets.QTableWidgetItem('Em progresso...'))
        widgets.tblLists.setItem(2, 0, QtWidgets.QTableWidgetItem('Concluida!'))
    
    def loadTopicsList(self):
        self.activeTable = 'tblTopics'
        widgets.tblLists.show()
        widgets.tblLists.setObjectName('tblTopics')
        widgets.lblSetInfo.setText('Tópico:')
        with DBMainOperations() as db:
            topicscount = db.cursor.execute("SELECT COUNT(*) FROM topics").fetchone()[0]
            widgets.tblLists.setRowCount(topicscount)
            topics = db.getAllRecords(tbl='topics')
            print(f'topics: {topics}')
        tablerow = 0
        for row in topics:
            widgets.tblLists.setItem(tablerow, 0, QtWidgets.QTableWidgetItem(row[1]))
            tablerow += 1

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
            sysdate = QtCore.QDate.currentDate().toString(QtCore.Qt.ISODate)
            newdata = (item.text(), "A começar", sysdate, sysdate, 0)
            with DBMainOperations() as db:
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
        with DBMainOperations() as db:
            topics = db.getAllRecords(tbl='topics', specifcols='topic_name')
        for topic in topics:
            item = QtWidgets.QListWidgetItem()
            item.setFlags(item.flags() | QtCore.Qt.ItemIsUserCheckable)
            item.setText(topic[0])
            item.setCheckState(QtCore.Qt.Unchecked)
            if topic[0] == '':
                item.setText('Sem tópico')
            widgets.listByTopic.addItem(item)

    def itemSelected(self):
        # item clicked
        pass

    def testCheck(self, item):  
        with DBMainOperations() as db:
            topicname = item.text()
            topicid = db.getAllRecords(tbl='topics', whclause=f'topic_name = "{topicname}"')[0][0]
        if item.checkState():
            self.orderByTopics.append(topicid)  # if checked, append in list to filter
        else:
            self.orderByTopics.remove(topicid)  # if unchecked, remove from list

        self.orderByState = False if len(self.orderByTopics) == 0 else True
        self.loadDataInTable(
            orderByTopic=self.orderByState, 
            topics=self.orderByTopics
        )
