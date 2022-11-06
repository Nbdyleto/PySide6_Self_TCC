from PySide6 import QtCore, QtGui, QtWidgets
from functions.db_main_operations import DBMainOperations

from functions.new_daily_task.ui_daily_task import Ui_DailyTaskPage

class DTaskMainPage(QtWidgets.QWidget):
    def __init__(self):
        super(DTaskMainPage, self).__init__()
        
        self.ui = Ui_DailyTaskPage()
        self.ui.setupUi(self)

        global widgets
        widgets = self.ui

        self.loadDataInTable()

        widgets.tblTasks.setColumnWidth(0,350)
        widgets.tblTasks.horizontalHeader().setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)
        widgets.tblTasks.horizontalHeader().setSectionResizeMode(2, QtWidgets.QHeaderView.Stretch)
        widgets.tblTasks.horizontalHeader().setSectionResizeMode(3, QtWidgets.QHeaderView.Stretch)
        widgets.tblTasks.horizontalHeader().setSectionResizeMode(4, QtWidgets.QHeaderView.Stretch)
        widgets.tblTasks.setColumnWidth(5,40)
        widgets.tblTasks.setStyleSheet("""
            QTableWidget::item{
                margin-top: 3px;          
                border-radius: 0px;
                padding-left: 15px;
                text-align: center;
            }
        """)

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