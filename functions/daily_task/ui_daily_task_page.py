# -*- coding: utf-8 -*-

################################################################################
## Widget generated from reading UI file 'main.ui'
##
## Created by: Qt User Interface Compiler version 6.3.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QMetaObject, QRect, Qt)
from PySide6.QtWidgets import (QCalendarWidget, QLabel, QTableWidget, QTableWidgetItem, QAbstractItemView)

class Ui_DailyTaskPage(object):
    def setupUi(self, Widget):
        if not Widget.objectName():
            Widget.setObjectName(u"Widget")
        Widget.resize(950, 514)

        self.tblTopics = QTableWidget(Widget)
        self.tblTopics.setGeometry(QRect(850, 200, 113, 100))
        self.tblTopics.setObjectName(u'tblTopics')
        self.tblTopics.setVisible(False)
        self.tblTopics.setColumnCount(1)
        self.tblTopics.setRowCount(1)
        item = QTableWidgetItem()
        self.tblTopics.setHorizontalHeaderItem(0, item)
        
        self.tblWidgetTasks = QTableWidget(Widget)
        self.tblWidgetTasks.setGeometry(QRect(140, 150, 950, 350))
        self.tblWidgetTasks.setObjectName(u"tblWidgetTasks")
        self.tblWidgetTasks.setSelectionMode(QAbstractItemView.NoSelection)
        self.tblWidgetTasks.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.tblWidgetTasks.setFocusPolicy(Qt.NoFocus)
        self.tblWidgetTasks.verticalHeader().setVisible(False)
        self.tblWidgetTasks.horizontalHeader().setVisible(True)
        self.tblWidgetTasks.setShowGrid(False)
        self.tblWidgetTasks.setSortingEnabled(False)
        self.tblWidgetTasks.setColumnCount(5)
        item = QTableWidgetItem()
        self.tblWidgetTasks.setHorizontalHeaderItem(0, item)
        item = QTableWidgetItem()
        self.tblWidgetTasks.setHorizontalHeaderItem(1, item)
        item = QTableWidgetItem()
        self.tblWidgetTasks.setHorizontalHeaderItem(2, item)
        item = QTableWidgetItem()
        self.tblWidgetTasks.setHorizontalHeaderItem(3, item)
        item = QTableWidgetItem()
        self.tblWidgetTasks.setHorizontalHeaderItem(4, item)

        ## Roxo
        self.tblWidgetTasks.setStyleSheet("""
            QTableWidget {
                background-color: rgb(40, 44, 52);
                border-radius: 0px;
            }
            QTableWidget::item {
                color: #f8f8f2;                    
                background-color: #44475a;
                margin-top: 2px;          
                border-radius: 0px;
                padding-left: 2px;
            }
            QTableWidget::item:selected {
                background-color: #6272a4;
                selection-color : #f8f8f2;  
            }
            QTableWidget::item:hover {
                background-color: #6272a4;
                color : #f8f8f2;
            }
        """)

        ## juco
        self.tblWidgetTasks.setStyleSheet("""
            QTableWidget {	
                background-color: transparent;
                border-radius: 0px;
            }
            QTableWidget::item{
                background-color: rgb(51, 61, 50);
                border-color: rgb(33, 51, 34);
                margin-top: 2px;          
                border-radius: 0px;
                padding-left: 2px;
            }
            QTableWidget::item:selected{
                background-color: rgb(162, 219, 85);
                color: black
            }
            QTableWidget::item:hover {
                background-color: rgb(162, 219, 85);
                color : black;
            }
            QHeaderView::section{
                background-color: rgb(36, 44, 35); 
                max-width: 30px;
                border: 1px solid rgb(51, 61, 50);
                border-style: none;
                border-bottom: 1px solid rgb(45, 48, 43);
                border-right: 1px solid rgb(45, 48, 43);
            }
            QHeaderView::section:vertical
            {
                border: 1px solid rgb(45, 48, 43);
            }
        """)

        self.calendarWidget = QCalendarWidget(Widget)
        self.calendarWidget.setObjectName(u"calendarWidget")
        self.calendarWidget.setGeometry(QRect(365, 205, 310, 220))
        self.calendarWidget.setVisible(False)
        self.calendarWidget.setStyleSheet("""
        QCalendarWidget QToolButton {
            height: 30px;
            width: 75px;
            color: #f8f8f2;
            font-size: 15px;
            icon-size: 15px;
            background-color: #44475a;
            margin-top: 1px;
        }
        QCalendarWidget QMenu {
            width: 150px;
            left: 20px;
            color: white;
            font-size: 15px;
            background-color: #44475a;
        }
        QCalendarWidget QSpinBox { 
            width: 50px; 
            font-size: 15px; 
            color: #f8f8f2; 
            padding-left: 19px;
            background-color: #44475a; 
            selection-background-color: #44475a;
            selection-color: #f8f8f2;
        }

        QCalendarWidget QSpinBox::up-button { 
            subcontrol-origin: border;  
            subcontrol-position: top right;  
            width:15px; 
        }
        QCalendarWidget QSpinBox::down-button {
            subcontrol-origin: border; 
            subcontrol-position: bottom right;  
            width:15px;
        }
        QCalendarWidget QSpinBox::up-arrow { 
            width:10px; 
            height:10px; 
        }
        QCalendarWidget QSpinBox::down-arrow { 
            width:10px; 
            height:10px; 
        }
        
        /* header row */
        QCalendarWidget QWidget { 
            alternate-background-color: #6272a4; 
        }
        
        /* normal days */
        QCalendarWidget QAbstractItemView:enabled 
        {
            font-size:15px;  
            color: #f8f8f2;  
            background-color: #44475a;  
            selection-background-color: #6272a4; 
            selection-color: black; 
        }
        
        /* days in other months */
        /* navigation bar */
        QCalendarWidget QWidget#qt_calendar_navigationbar
        { 
            background-color: #44475a; 
        }

        QCalendarWidget QAbstractItemView:disabled 
        { 
            color: #6272a4; 
        }

        """)

        self.tblTopics = QTableWidget(Widget)
        self.tblTopics.setGeometry(QRect(900, 205, 140, 190))
        self.tblTopics.setObjectName(u'tblTopics')
        self.tblTopics.setVisible(False)
        self.tblTopics.setColumnCount(1)
        self.tblTopics.setRowCount(1)
        item = QTableWidgetItem()
        self.tblTopics.setHorizontalHeaderItem(0, item)
        self.tblTopics.setFocusPolicy(Qt.NoFocus)
        self.tblTopics.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tblTopics.setSelectionMode(QAbstractItemView.SingleSelection)
        self.tblTopics.verticalHeader().setVisible(False)
        self.tblTopics.horizontalHeader().setVisible(False)
        self.tblTopics.setShowGrid(False)
        self.tblTopics.setSortingEnabled(False)
        self.tblWidgetTasks.setWordWrap(True)
        self.tblTopics.setStyleSheet("""
            QTableWidget {
                background-color:#282a36;
                selection-color: #000000; 
            }
            QTableWidget::item {
                color: #f8f8f2;                    
                background-color: #282a36;
                margin-top: 0px;         
                padding-left: 2px;
            }
            QTableWidget::item:hover {
                background-color: #6272a4;
                

            }
        """)

        self.tblStatus = QTableWidget(Widget)
        self.tblStatus.setGeometry(QRect(450, 205, 130, 115))
        self.tblStatus.setObjectName(u'tblTopics')
        self.tblStatus.setVisible(False)
        self.tblStatus.setColumnCount(1)
        self.tblStatus.setRowCount(1)
        item = QTableWidgetItem()
        self.tblStatus.setHorizontalHeaderItem(0, item)
        self.tblStatus.setFocusPolicy(Qt.NoFocus)
        self.tblStatus.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tblStatus.setSelectionMode(QAbstractItemView.SingleSelection)
        self.tblStatus.verticalHeader().setVisible(False)
        self.tblStatus.horizontalHeader().setVisible(False)
        self.tblStatus.setShowGrid(False)
        self.tblStatus.setSortingEnabled(False)
        self.tblWidgetTasks.setWordWrap(True)
        self.tblStatus.setStyleSheet("""
            QTableWidget {
                background-color:#282a36;
                selection-color: #000000; 
            }
            QTableWidget::item {
                color: #f8f8f2;                    
                background-color: #282a36;
                margin-top: 0px;         
                padding-left: 2px;
            }
            QTableWidget::item:hover {
                background-color: #6272a4;
                

            }
        """)

        self.retranslateUi(Widget)
        QMetaObject.connectSlotsByName(Widget)
    # setupUi

    def retranslateUi(self, Widget):
        _translate = QCoreApplication.translate
        Widget.setWindowTitle(_translate("Widget", u"Widget", None))
        item = self.tblWidgetTasks.horizontalHeaderItem(0)
        item.setText(_translate("Widget", u"Nome da Tarefa"))
        item = self.tblWidgetTasks.horizontalHeaderItem(1)
        item.setText(_translate("Widget", u"Status"))
        item = self.tblWidgetTasks.horizontalHeaderItem(2)
        item.setText(_translate("Widget", u"Data Inicial"))
        item = self.tblWidgetTasks.horizontalHeaderItem(3)
        item.setText(_translate("Widget", u"Data Final"))
        item = self.tblWidgetTasks.horizontalHeaderItem(4)
        item.setText(_translate("Widget", u"Tópico"))
        item = self.tblTopics.horizontalHeaderItem(0)
        item.setText(_translate("Widget", u"topic_name"))
    # retranslateUi

