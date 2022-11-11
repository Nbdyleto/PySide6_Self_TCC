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
        global widgets
        widgets = self.ui

    def setupConnections(self):
        widgets.tblTasks.cellClicked.connect(self.rowClickedFunctions)

    def setupWidgets(self):
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

    def loadDataInTable(self):
        widgets.tblTasks.clearContents()
        with DBMainOperations() as db:
            taskscount = db.cursor.execute("SELECT COUNT(*) FROM tasks").fetchone()[0]
            widgets.tblTasks.setRowCount(taskscount+1)
            #topicscount = db.cursor.execute("SELECT COUNT(*) FROM topics").fetchone()[0]
            #tblTopics.setRowCount(topicscount+1)
            topics = db.cursor.execute("SELECT * FROM topics").fetchall()
            tasks = db.cursor.execute("SELECT * FROM tasks ORDER BY start_date").fetchall()
        try:
            tablerow = 0
            for row in tasks:
                widgets.tblTasks.setRowHeight(tablerow, 50)
                #startDate, endDate = self.formatDate(row[2], row[3])
                widgets.tblTasks.setItem(tablerow, 0, QtWidgets.QTableWidgetItem(row[0]))  #row[0] = task_name
                widgets.tblTasks.setItem(tablerow, 1, QtWidgets.QTableWidgetItem(row[1]))  #row[1] = status
                widgets.tblTasks.setItem(tablerow, 2, QtWidgets.QTableWidgetItem('startDate')) #row[3] = start_date
                widgets.tblTasks.setItem(tablerow, 3, QtWidgets.QTableWidgetItem('endDate')) #row[4] = end_date
                widgets.tblTasks.setItem(tablerow, 4, QtWidgets.QTableWidgetItem('self.topics[row[4]][1]')) #row[4] = topic_id
                tablerow += 1
                
            widgets.tblTasks.setRowHeight(tablerow, 50)
        except Exception:
            print('ERROR')
    
    # Row functions

    def rowClickedFunctions(self, row, col):
        if self.isExistentInDB(row) and col != 0:
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

    def isExistentInDB(self, row):
        self.hideAll()
        with DBMainOperations() as db:
            try:
                selectedrow = widgets.tblTasks.item(row, 0).text()
                db.getAllRecords(tbl='tasks', specifcols='task_name', whclause=f'task_name = "{selectedrow}"')
                print('existent!')
                return True
            except Exception:
                print('not existent!')
                return False

    def hideAll(self):
        widgets.tblLists.clearContents()
        widgets.qCalendar.clearMask()
        widgets.lblSetInfo.setVisible(False)
        widgets.qCalendar.setVisible(False)
        widgets.tblLists.setVisible(False)
        widgets.lblSetInfo.setVisible(False)

    def loadStatusList(self):
        widgets.lblSetInfo.setText('Status:')
        widgets.tblLists.show()
        widgets.tblLists.setRowCount(3)
        widgets.tblLists.setItem(0, 0, QtWidgets.QTableWidgetItem('Não iniciada.'))
        widgets.tblLists.setItem(1, 0, QtWidgets.QTableWidgetItem('Em progresso...'))
        widgets.tblLists.setItem(2, 0, QtWidgets.QTableWidgetItem('Concluida!'))
    
    def loadTopicsList(self):
        widgets.tblLists.show()
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
        widgets.lblSetInfo.setText('Data Inicial:')
        widgets.qCalendar.show()

    def showEndDate(self):
        widgets.lblSetInfo.setText('Data Final:')
        widgets.qCalendar.show()