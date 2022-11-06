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
                padding-left: 5px;
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
        btnStartStudy, btnAddCards = None, None

        btnEditCards = QtWidgets.QPushButton(widgets.tblDecks)
        btnEditCards.setMinimumSize(QtCore.QSize(0, 100))
        btnEditCards.setMaximumSize(QtCore.QSize(90, 16777215))
        btnEditCards.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        btnEditCards.setLayoutDirection(QtCore.Qt.LeftToRight)
        btnEditCards.setObjectName(f'btnEditCards{tablerow}')
        btnEditCards.setStyleSheet(u"""
                background-position: center; 
                background-repeat: no-repeat; 
                background-image: url(:/icons/images/icons/cil-pencil.png);
                border-radius: 45px;
                border-color: transparent;
        """)
        widgets.tblDecks.setCellWidget(tablerow, 2, btnEditCards)

        btnEditDeck = QtWidgets.QPushButton(widgets.tblDecks)
        btnEditDeck.setMinimumSize(QtCore.QSize(0, 100))
        btnEditDeck.setMaximumSize(QtCore.QSize(90, 16777215))
        btnEditDeck.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        btnEditDeck.setLayoutDirection(QtCore.Qt.LeftToRight)
        btnEditDeck.setObjectName(f'btnEditDecks{tablerow}')
        btnEditDeck.setStyleSheet(u"""
                background-position: center; 
                background-repeat: no-repeat; 
                background-image: url(:/icons/images/icons/cil-options.png);
                border-radius: 45px;
                border-color: transparent;
        """)
        widgets.tblDecks.setCellWidget(tablerow, 3, btnEditDeck)

        with DBMainOperations() as db:
            print(db.hasRecordsInTblFlashcards(id=tablerow))
            if db.hasRecordsInTblFlashcards(id=tablerow):
                btnStartStudy = QtWidgets.QPushButton(widgets.tblDecks)
                btnStartStudy.setMinimumSize(QtCore.QSize(0, 100))
                btnStartStudy.setMaximumSize(QtCore.QSize(90, 16777215))
                btnStartStudy.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
                btnStartStudy.setLayoutDirection(QtCore.Qt.LeftToRight)
                btnStartStudy.setObjectName(f'btnStartStudy{tablerow}')
                btnStartStudy.setStyleSheet(u"""
                    background-position: center; 
                    background-repeat: no-repeat; 
                    background-image: url(:/icons/images/icons/cil-media-play.png);
                    border-radius: 45px;
                    border-color: transparent;
                """)
                widgets.tblDecks.setCellWidget(tablerow, 4, btnStartStudy)
                btnStartStudy.clicked.connect(lambda: self.openStudyCardsWindow(row_clicked=tablerow))
            else:
                btnAddCards = QtWidgets.QPushButton(widgets.tblDecks)
                btnAddCards.setMinimumSize(QtCore.QSize(0, 100))
                btnAddCards.setMaximumSize(QtCore.QSize(90, 16777215))
                btnAddCards.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
                btnAddCards.setLayoutDirection(QtCore.Qt.LeftToRight)
                btnAddCards.setObjectName(f'btnAddCards{tablerow}')
                btnAddCards.setStyleSheet(u"""
                    background-position: center; 
                    background-repeat: no-repeat; 
                    background-image: url(:/icons/images/icons/cil-plus.png);
                    border-radius: 45px;
                    border-color: transparent;
                """)
                widgets.tblDecks.setCellWidget(tablerow, 4, btnAddCards)
                btnAddCards.clicked.connect(lambda: self.openAddCardsWindow(row_clicked=tablerow))