from ast import With
from sqlite3 import dbapi2
from PySide6.QtWidgets import QWidget, QApplication, QAbstractItemView, QListWidgetItem, QTableWidgetItem, QMessageBox, QCheckBox
from PySide6.QtCore import QDate, QPoint, QSize
from PySide6.QtGui import QBrush, QColor, QIcon, Qt
from .ui_daily_task_page import Ui_DailyTaskPage
from .tasks_db_operations import DailyTaskDB

import sys

class DTaskMainPage(QWidget):
    def __init__(self):
        super(DTaskMainPage, self).__init__()
        
        self.ui = Ui_DailyTaskPage()
        self.ui.setupUi(self)

        global widgets
        widgets = self.ui

        widgets.tblWidgetTasks.setColumnWidth(0,300)
        widgets.tblWidgetTasks.setColumnWidth(1,150)
        widgets.tblWidgetTasks.setColumnWidth(2,150)
        widgets.tblWidgetTasks.setColumnWidth(3,150)
        widgets.tblWidgetTasks.setColumnWidth(4,150)

        with DailyTaskDB() as db:
            db.create_tables()
        
        self.load_data_in_table()

        widgets.calendarWidget.selectionChanged.connect(self.calendar_date_changed)
        self.selected_task = None
        self.existent_in_db = False
        self.slc_start_date = QDate.currentDate().toString(Qt.ISODate)
        self.slc_end_date = QDate.currentDate().toString(Qt.ISODate)
        self.slc_date_cel = []
        self.slc_topic_index = 0

        widgets.tblWidgetTasks.cellClicked.connect(self.is_existent_in_db)
        widgets.tblWidgetTasks.itemChanged.connect(self.update_db)

        widgets.tblTopics.cellClicked.connect(self.select_topic)

        self.slc_row, self.slc_col = None, None

        self.colors_list = ['#44475a', '#705D8C', '#BB6BBF', '#A366FF', '#7666FF', '#8C80FF']

    @property
    def row_tasks_count(self):
        return getattr(self, '_row_tasks_count', 1)
        
    @row_tasks_count.setter
    def row_tasks_count(self, val):
        self._row_tasks_count = val

    @property
    def topics(self):
        return getattr(self, '_topics', '')
    
    @topics.setter
    def topics(self, values):
        self._topics = values
    
    @property
    def row_topics_count(self):
        return getattr(self, '_row_topics_count', 1)
    
    @row_topics_count.setter
    def row_topics_count(self, val):
        self._row_topics_count = val

    def load_data_in_table(self):
        widgets.tblWidgetTasks.clearContents()

        with DailyTaskDB() as db:
            count = db.cursor.execute("SELECT COUNT(*) FROM tasks").fetchone()[0]
            self.row_tasks_count = count+1
            widgets.tblWidgetTasks.setRowCount(self.row_tasks_count)

            count = db.cursor.execute("SELECT COUNT(*) FROM topics").fetchone()[0]
            self.row_topics_count = count+1
            widgets.tblTopics.setRowCount(self.row_topics_count)

            self.topics = db.cursor.execute("SELECT * FROM topics").fetchall()
            print(self.topics)

            results = db.cursor.execute("SELECT * FROM tasks ORDER BY start_date").fetchall()
        print(f'results:{results}')

        try:
            tablerow = 0
            for row in results:
                print(str(row[2]))
                
                widgets.tblWidgetTasks.setItem(tablerow, 0, QTableWidgetItem(row[0]))  #row[0] = task_name
                widgets.tblWidgetTasks.setItem(tablerow, 1, QTableWidgetItem(row[1]))  #row[1] = status
                widgets.tblWidgetTasks.setItem(tablerow, 2, QTableWidgetItem(row[2]))  #row[2] = start_date
                widgets.tblWidgetTasks.setItem(tablerow, 3, QTableWidgetItem(row[3]))  #row[3] = end_date
                widgets.tblWidgetTasks.setItem(tablerow, 4, QTableWidgetItem(self.topics[row[4]][1])) #row[4] = topic_id
                tablerow += 1
        except Exception:
            print('Não funfou.')

        #widgets.tblWidgetTasks.setRowHeight(0, 100)

    # atributtes from each task:
    # name, topic, start_date, limit_date, checked.

    def update_db(self, item, is_date_type = False):
        if self.existent_in_db == None:
            return  # Block Uselless Process
        else:
            row, col = item.row(), item.column()
            new_value = item.text()
            task_name = self.selected_task
            start_date = self.slc_start_date
            end_date = self.slc_end_date
            topic_id = self.slc_topic_index

            if is_date_type:
                if self.slc_col == 2:
                    new_value = start_date
                elif self.slc_col == 3:
                    new_value = end_date
                else:
                    self.slc_start_date, self.slc_end_date = None, None
            
            if self.slc_col == 4:
                new_value = topic_id

            field_list = ['task_name', 'status', 'start_date', 'end_date', 'topic_id']
            act_field = field_list[col]

            #print(item.row(), item.column())
            print(f'actual field: {item.text()}')

            print('NOVA EXECUÇÃO...')
            print(f'new value:{new_value, self.existent_in_db}\n')
            
            if self.existent_in_db:
                # existent in db, so, update old data.
                query_update = f"UPDATE tasks SET {act_field} = '{new_value}' WHERE task_name = '{task_name}'"
                print(query_update)
                with DailyTaskDB() as db:
                    db.cursor.execute(query_update)
                self.existent_in_db = None
                self.load_data_in_table()
                        
            if self.existent_in_db == False: 
                # not existent in db, so, create new data.
                query_insert = f"INSERT INTO tasks(task_name, status, start_date, end_date, topic_id) VALUES (?,?,?,?,?)"
                new_row_data = (new_value, "A começar", start_date, end_date, 0)
                with DailyTaskDB() as db:
                    db.populate(query_insert, new_row_data)
                self.existent_in_db = None
                self.load_data_in_table()

    def is_existent_in_db(self, row, col):
        query = 'SELECT task_name FROM tasks WHERE task_name = ?'
        try:
            self.selected_task = widgets.tblWidgetTasks.item(row, 0).text() # task name.
            self.selected_task_data = widgets.tblWidgetTasks.item(row, col).text()
            with DailyTaskDB() as db:
                db.cursor.execute(query, [self.selected_task])
            print(f'task_name: {self.selected_task} EXISTENT!')
            self.existent_in_db = True
        except Exception:
            print('NOT EXISTENT!')
            self.existent_in_db = False
        print(self.existent_in_db, '\n')

        self.slc_row, self.slc_col = row, col

        if ((col == 2 or col == 3) and self.existent_in_db == True): # start_date or end_date cells
            self.show_calendar()
            self.hide_topics()
        elif col == 4 and self.existent_in_db == True:  # topics cell
            self.show_topics()
            self.hide_calendar()
        else:
            self.hide_calendar()
            self.hide_topics()

    ############# CALENDAR CELLS 'CLICKED' FUNCTIONS

    def show_calendar(self):
        self.reset_calendar_date()
        widgets.calendarWidget.setVisible(True)
        X_VALUE, Y_VALUE = 365, 205
        if self.slc_col == 3:
            X_VALUE = 450
        widgets.calendarWidget.move(X_VALUE, Y_VALUE)
        print(f'showing calendar... {self.slc_row, self.slc_col}')

    def hide_calendar(self):
        widgets.calendarWidget.setVisible(False)

    def reset_calendar_date(self):
        self.slc_start_date = QDate.currentDate().toString(Qt.ISODate) # Qt.RFC2822Date
        self.slc_end_date = QDate.currentDate().toString(Qt.ISODate)
        print('reseting...')

    def calendar_date_changed(self):
        self.hide_calendar()
        print('the calendar date has changed! \n')

        if self.slc_col == 2:  #start_date cell
            self.slc_start_date = widgets.calendarWidget.selectedDate().toString(Qt.ISODate)
        elif self.slc_col == 3: # end_date cell
            self.slc_end_date = widgets.calendarWidget.selectedDate().toString(Qt.ISODate)
        else:
            print('None')

        print(f'new date: {self.slc_start_date}')
        item = widgets.tblWidgetTasks.item(self.slc_row, self.slc_col)
        self.update_db(item, is_date_type=True)
        self.reset_calendar_date()

    ############# TOPICS CELL 'CLICKED' FUNCTIONS
    
    def show_topics(self):
        widgets.tblTopics.setVisible(True)
        self.load_topics()
        print('showing topics')
    
    def hide_topics(self):
        widgets.tblTopics.setVisible(False)
    
    def load_topics(self):
        widgets.tblTopics.clearContents()
        print('loading topics')
        tablerow = 0
        widgets.tblTopics.setRowCount(len(self.topics)+1)
        print(self.topics)
        for row in self.topics:
            print(row)
            widgets.tblTopics.setItem(tablerow, 0, QTableWidgetItem(row[1]))
            tablerow += 1
    
    def select_topic(self, row, col):
        if row == self.row_topics_count-1:  # last row
            widgets.tblTopics.itemChanged.connect(self.update_topics)
        else:
            self.slc_topic_index = row
            self.hide_topics()
            item = widgets.tblWidgetTasks.item(self.slc_row, self.slc_col)
            self.update_db(item)

    def update_topics(self, item):
        widgets.tblTopics.itemChanged.disconnect() # <- not elegant, appearently 
        
        self.row_topics_count += 1
        topic_id = self.row_topics_count
        new_value = item.text()
        
        query_insert = f"INSERT INTO topics (topic_id, topic_name) VALUES (?, ?)"
        new_row_data = (topic_id, new_value)
        with DailyTaskDB() as db:
            db.populate(query_insert, new_row_data)
            self.topics = db.cursor.execute("SELECT * FROM topics").fetchall() # update topics property
        self.load_topics()
        # self.select_topic(item.row(), item.col())   # Study 'Slots' to work with this 

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = DTaskMainPage()
    window.setStyleSheet('background-color: #282a36;')
    window.show()
    sys.exit(app.exec())