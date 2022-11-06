from PySide6 import QtCore, QtGui, QtWidgets
from functions.db_main_operations import DBMainOperations

from functions.test_ui.ui_test import Ui_Widget

class MainTestPage(QtWidgets.QWidget):
    def __init__(self):
        super(MainTestPage, self).__init__()
        self.ui = Ui_Widget()
        self.ui.setupUi(self)

        global widgets
        widgets = self.ui

        widgets.tblDecks.setRowCount(10)

        self.loadDecksInTable()

        widgets.tblDecks.horizontalHeader().setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
        widgets.tblDecks.setColumnWidth(1,400)
        widgets.tblDecks.horizontalHeader().setSectionResizeMode(2, QtWidgets.QHeaderView.Stretch)
        widgets.tblDecks.horizontalHeader().setSectionResizeMode(3, QtWidgets.QHeaderView.Stretch)
        widgets.tblDecks.horizontalHeader().setSectionResizeMode(4, QtWidgets.QHeaderView.Stretch)
        widgets.tblDecks.horizontalHeader().setSectionResizeMode(5, QtWidgets.QHeaderView.Stretch)
        widgets.tblDecks.setStyleSheet("""
            QTableWidget::item{
                margin-top: 3px;          
                border-radius: 0px;
                padding-left: 15px;
                text-align: center;
            }
        """)
        
    def loadDecksInTable(self):
        with DBMainOperations() as db:
            rowcount = db.getRowCount(tbl='decks')
            decks = db.getAllRecords(tbl='decks')
        widgets.tblDecks.clearContents()
        widgets.tblDecks.setRowCount(rowcount)
        
        tablerow = 0
        for deck in decks:
            widgets.tblDecks.setRowHeight(tablerow, 100)
            widgets.tblDecks.setItem(tablerow, 0, QtWidgets.QTableWidgetItem(f'{str(deck[2])}%'))
            widgets.tblDecks.setItem(tablerow, 1, QtWidgets.QTableWidgetItem(deck[1]))
            self.loadWidgetCell(tablerow)
            tablerow+=1
            
            
    def loadWidgetCell(self, tablerow):
        self.btnStartStudy, self.btnAddCards = None, None

        self.btnEditCards = QtWidgets.QPushButton(widgets.tblDecks)
        self.btnEditCards.setMinimumSize(QtCore.QSize(0, 100))
        self.btnEditCards.setMaximumSize(QtCore.QSize(90, 16777215))
        self.btnEditCards.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.btnEditCards.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.btnEditCards.setObjectName(f'btnEditCards{tablerow}')
        self.btnEditCards.setStyleSheet(u"""
                background-position: center; 
                background-repeat: no-repeat; 
                background-image: url(:/icons/images/icons/cil-pencil.png);
                border-radius: 45px;
                border-color: transparent;
        """)
        widgets.tblDecks.setCellWidget(tablerow, 2, self.btnEditCards)

        self.btnEditDecks = QtWidgets.QPushButton(widgets.tblDecks)
        self.btnEditDecks.setMinimumSize(QtCore.QSize(0, 100))
        self.btnEditDecks.setMaximumSize(QtCore.QSize(90, 16777215))
        self.btnEditDecks.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.btnEditDecks.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.btnEditDecks.setObjectName(f'btnEditDecks{tablerow}')
        self.btnEditDecks.setStyleSheet(u"""
                background-position: center; 
                background-repeat: no-repeat; 
                background-image: url(:/icons/images/icons/cil-options.png);
                border-radius: 45px;
                border-color: transparent;
        """)
        widgets.tblDecks.setCellWidget(tablerow, 3, self.btnEditDecks)

        with DBMainOperations() as db:
            print(db.hasRecordsInTblFlashcards(id=tablerow))
            if db.hasRecordsInTblFlashcards(id=tablerow):
                self.btnStartStudy = QtWidgets.QPushButton(widgets.tblDecks)
                self.btnStartStudy.setMinimumSize(QtCore.QSize(0, 100))
                self.btnStartStudy.setMaximumSize(QtCore.QSize(90, 16777215))
                self.btnStartStudy.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
                self.btnStartStudy.setLayoutDirection(QtCore.Qt.LeftToRight)
                self.btnStartStudy.setObjectName(f'btnStartStudy{tablerow}')
                self.btnStartStudy.setStyleSheet(u"""
                    background-position: center; 
                    background-repeat: no-repeat; 
                    background-image: url(:/icons/images/icons/cil-media-play.png);
                    border-radius: 45px;
                    border-color: transparent;
                """)
                widgets.tblDecks.setCellWidget(tablerow, 4, self.btnStartStudy)
                #self.btnStartStudy.clicked.connect(lambda: self.openStudyCardsWindow(row_clicked=tablerow))
            else:
                self.btnAddCards = QtWidgets.QPushButton(widgets.tblDecks)
                self.btnAddCards.setMinimumSize(QtCore.QSize(0, 100))
                self.btnAddCards.setMaximumSize(QtCore.QSize(90, 16777215))
                self.btnAddCards.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
                self.btnAddCards.setLayoutDirection(QtCore.Qt.LeftToRight)
                self.btnAddCards.setObjectName(f'btnAddCards{tablerow}')
                self.btnAddCards.setStyleSheet(u"""
                    background-position: center; 
                    background-repeat: no-repeat; 
                    background-image: url(:/icons/images/icons/cil-plus.png);
                    border-radius: 45px;
                    border-color: transparent;
                """)
                widgets.tblDecks.setCellWidget(tablerow, 4, self.btnAddCards)
                #self.btnAddCards.clicked.connect(lambda: self.openAddCardsWindow(row_clicked=tablerow))
