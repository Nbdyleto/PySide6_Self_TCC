from PySide6 import QtCore, QtGui, QtWidgets
from functions.db_main_operations import DBMainOperations

from functions.new_pomodoro.ui_pomodoro_page import Ui_Widget

class NewPomodoroMainPage(QtWidgets.QWidget):
    def __init__(self):
        super(NewPomodoroMainPage, self).__init__()
        
        self.ui = Ui_Widget()
        self.ui.setupUi(self)

        global widgets
        widgets = self.ui

        widgets.tblTasks.horizontalHeader().setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
        widgets.tblTasks.horizontalHeader().setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)

        timeFormat = "hh:mm:ss"
        test = QtCore.QTime(0, 10, 0) 
        widgets.lcdPomodoroTimer.display(test.toString(timeFormat))

    def loadDataInTable(self):
        widgets.tblTasks.clearContents()
        with DBMainOperations() as db:
            taskscount = db.cursor.execute("SELECT COUNT(*) FROM tasks").fetchone()[0]
            widgets.tblTasks.setRowCount(taskscount+1)
            topics = db.cursor.execute("SELECT * FROM topics").fetchall()
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