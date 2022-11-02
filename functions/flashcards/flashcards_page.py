import os
from pathlib import Path
import sys

from PySide6 import QtCore, QtGui, QtWidgets
from PySide6.QtWidgets import QWidget, QApplication, QSizePolicy

from .ui_flashcards_page import Ui_FlashcardsPage
from .ui_add_cards import Ui_AddCardsWindow
from .ui_study_cards import Ui_StudyCardsWindow

from ..db_main_operations import DBMainOperations

import random

class FCardsMainPage(QWidget):
    def __init__(self):
        super(FCardsMainPage, self).__init__()
        self.ui = Ui_FlashcardsPage()
        self.ui.setupUi(self)

        global widgets
        widgets = self.ui

        self.addCardsWindow = None
        
        self.loadDecksInTable()
        widgets.btnAddCards.clicked.connect(self.openAddCardsWindow)

        self.reveal_pressed = False
        self.studed_cards = 0
    
    # MainWindow Functions

    def loadDecksInTable(self):
        with DBMainOperations() as db:
            rowcount = db.getRowCount(tbl='decks')
            decks = db.getAllRecords(tbl='decks')
        widgets.tblWidgetDecks.clearContents()
        widgets.tblWidgetDecks.setRowCount(rowcount+1)
        
        tablerow = 0
        for deck in decks:
            widgets.tblWidgetDecks.setRowHeight(tablerow, 100)
            widgets.tblWidgetDecks.setItem(tablerow, 1, QtWidgets.QTableWidgetItem(f'{str(deck[2])}%'))
            widgets.tblWidgetDecks.setItem(tablerow, 2, QtWidgets.QTableWidgetItem(deck[1]))
            self.loadWidgetCell(tablerow)
            tablerow+=1
            
        # last row of tblWidget has a 'add deck' option.
        lastrow = rowcount
        widgets.tblWidgetDecks.setRowHeight(tablerow, 100)
        widgets.tblWidgetDecks.setItem(lastrow, 2, QtWidgets.QTableWidgetItem('Criar novo deck!'))
        
        btnAddDeck = QtWidgets.QPushButton(widgets.tblWidgetDecks)
        btnAddDeck.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        btnAddDeck.setLayoutDirection(QtCore.Qt.LeftToRight)
        btnAddDeck.setStyleSheet(u"""
            background-position: center; 
            background-repeat: no-repeat; 
            background-image: url(:/icons/images/icons/cil-library-add.png);
            border-radius: 45px;
        """)
        widgets.tblWidgetDecks.setCellWidget(lastrow, 1, btnAddDeck)
        widgets.tblWidgetDecks.cellWidget(lastrow, 1).clicked.connect(self.addDeck)

    def loadWidgetCell(self, tablerow):
        btnStartStudy, btnAddCards = None, None

        btnEditCards = QtWidgets.QPushButton(widgets.tblWidgetDecks)
        btnEditCards.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        btnEditCards.setLayoutDirection(QtCore.Qt.LeftToRight)
        btnEditCards.setObjectName(f'btnEditCards{tablerow}')
        btnEditCards.setStyleSheet(u"""
                background-position: center; 
                background-repeat: no-repeat; 
                background-image: url(:/icons/images/icons/cil-pencil.png);
                border-radius: 45px;
        """)
        widgets.tblWidgetDecks.setCellWidget(tablerow, 4, btnEditCards)

        btnEditDeck = QtWidgets.QPushButton(widgets.tblWidgetDecks)
        btnEditDeck.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        btnEditDeck.setLayoutDirection(QtCore.Qt.LeftToRight)
        btnEditDeck.setObjectName(f'btnEditDecks{tablerow}')
        btnEditDeck.setStyleSheet(u"""
                background-position: center; 
                background-repeat: no-repeat; 
                background-image: url(:/icons/images/icons/cil-options.png);
                border-radius: 45px;
        """)
        widgets.tblWidgetDecks.setCellWidget(tablerow, 5, btnEditDeck)

        with DBMainOperations() as db:
            print(db.hasRecordsInTblFlashcards(id=tablerow))
            if db.hasRecordsInTblFlashcards(id=tablerow):
                btnStartStudy = QtWidgets.QPushButton(widgets.tblWidgetDecks)
                btnStartStudy.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
                btnStartStudy.setLayoutDirection(QtCore.Qt.LeftToRight)
                btnStartStudy.setObjectName(f'btnStartStudy{tablerow}')
                btnStartStudy.setStyleSheet(u"""
                    background-position: center; 
                    background-repeat: no-repeat; 
                    background-image: url(:/icons/images/icons/cil-media-play.png);
                    border-radius: 45px;
                """)
                widgets.tblWidgetDecks.setCellWidget(tablerow, 3, btnStartStudy)
                btnStartStudy.clicked.connect(lambda: self.openStudyCardsWindow(row_clicked=tablerow))
            else:
                btnAddCards = QtWidgets.QPushButton(widgets.tblWidgetDecks)
                btnAddCards.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
                btnAddCards.setLayoutDirection(QtCore.Qt.LeftToRight)
                btnAddCards.setObjectName(f'btnAddCards{tablerow}')
                btnAddCards.setStyleSheet(u"""
                    background-position: center; 
                    background-repeat: no-repeat; 
                    background-image: url(:/icons/images/icons/cil-plus.png);
                    border-radius: 45px;
                    margin-topd
                """)
                widgets.tblWidgetDecks.setCellWidget(tablerow, 3, btnAddCards)
                btnAddCards.clicked.connect(lambda: self.openAddCardsWindow(row_clicked=tablerow))
    
    @QtCore.Slot()
    def addDeck(self):
        new_deck, input_status = QtWidgets.QInputDialog.getText(self, "Novo Deck", "Entre com o nome do novo deck:")
        with DBMainOperations() as db:
            if input_status:
                last_id = db.getRowCount('decks')
                db.populateTbl(tbl='decks', params=(last_id, new_deck, 0, 0))
        self.loadDecksInTable()

    # AddCardsWindow Functions #####################################
    
    @QtCore.Slot()
    def openAddCardsWindow(self, row_clicked):
        self.addCardsWindow = QtWidgets.QMainWindow()
        self.ui_addCards = Ui_AddCardsWindow()
        self.ui_addCards.setupUi(self.addCardsWindow)

        global cardsWinWidgets
        cardsWinWidgets = self.ui_addCards

        cardsWinWidgets.listDecks.setCurrentRow(0)
        self.addCardsWindow.show()
        cardsWinWidgets.btnAddCard.clicked.connect(self.addCards)

        self.loadDecksList()
    
    def loadDecksList(self):
        with DBMainOperations() as db:
            decks = db.getAllRecords(tbl='decks', specifcols='deck_name', fetchall=True)
        print(decks)
        for deck_name in decks:
            cardsWinWidgets.listDecks.addItem(deck_name[0])

    @QtCore.Slot()
    def addCards(self):
        card_question = cardsWinWidgets.pTextFront.toPlainText()
        card_answer = cardsWinWidgets.pTextVerse.toPlainText()
        if card_question and card_answer != "":
            deck_id = cardsWinWidgets.listDecks.currentRow()
            card_question = cardsWinWidgets.pTextFront.toPlainText()
            card_answer = cardsWinWidgets.pTextVerse.toPlainText()
            with DBMainOperations() as db:
                print('populating...')
                db.populateTbl(tbl='flashcards', params=(card_question, card_answer, deck_id))
            self.winAddCardsClearContents()
            self.loadDecksInTable()
        else:
            retry_msg = QtWidgets.QMessageBox(self.addCardsWindow)
            retry_msg.setStyleSheet("color: #44475a")
            retry_msg.setText('Input something in your card (front and verse)!')
            retry_msg.show()

    def winAddCardsClearContents(self):
        cardsWinWidgets.pTextFront.clear()
        cardsWinWidgets.pTextVerse.clear()

    # StudyCards Functions #################################

    @QtCore.Slot()
    def openStudyCardsWindow(self, row_clicked):
        self.studyCardsWindow = QtWidgets.QMainWindow()
        self.ui_studyCards = Ui_StudyCardsWindow()
        self.ui_studyCards.setupUi(self.studyCardsWindow)

        global studyCardsWidgets
        studyCardsWidgets = self.ui_studyCards

        self.infoStudyCardsWindow(row_clicked)
        self.card_iterator = None
        self.infoStudyCards(deck_id=row_clicked)

        self.studyCardsWindow.show()

    def infoStudyCardsWindow(self, row_clicked):
        self.pValue = 0
        print('row_clicked: ', row_clicked)
        with DBMainOperations() as db:
            records = db.getAllRecords(tbl='decks', specifcols='deck_name, hits_percentage', 
                                       fetchall=True, whclause=f'deck_id={row_clicked}')
            self.total_cards = db.getRowCount(tbl='flashcards', whclause=f'deck_id={row_clicked}')
        deck_name = records[0][0]
        studyCardsWidgets.lblDeckName.setText(deck_name)
        hits_percentage = records[0][1]
        studyCardsWidgets.pBarHitsPercentage.setValue(hits_percentage)
        
    def infoStudyCards(self, pValue=0, reveal_pressed=False, deck_id=None):
        print(self.total_cards)
        if reveal_pressed:
            self.studed_cards += 1
        studyCardsWidgets.btnRevealAnswer.setVisible(True)
        studyCardsWidgets.btnUnsatisfactory.setVisible(False)
        studyCardsWidgets.btnNormal.setVisible(False)
        studyCardsWidgets.btnVeryGood.setVisible(False)
        self.pValue += pValue
        studyCardsWidgets.pBarHitsPercentage.setValue(pValue)

        if self.card_iterator is None:
            # Create a card_iterator if no exists (always the studyCards page is called from Window).
            self.studed_cards = 1
            with DBMainOperations() as db:
                cards = db.getAllRecords(tbl='flashcards', specifcols='card_question, card_answer',
                                         fetchall=True, whclause=f'deck_id = {deck_id}')
            random.shuffle(cards)
            self.card_iterator = iter(cards)

        try:
            front, verse = next(self.card_iterator)
            studyCardsWidgets.plainTextEdit.setPlainText(front)
            studyCardsWidgets.btnRevealAnswer.clicked.connect(lambda: self.revealCardAnswer(verse))
            studyCardsWidgets.lblCardsQnt.setText(f"{self.studed_cards}/{str(self.total_cards)}")
        except:
            print('studed_cards:',self.studed_cards)
            if self.studed_cards > self.total_cards+8:
                self.studyCardsWindow.close()
            print('Stop Iteration')

    def revealCardAnswer(self, verse):
        studyCardsWidgets.plainTextEdit.setPlainText(verse)
        studyCardsWidgets.btnUnsatisfactory.clicked.connect(lambda: self.infoStudyCards(pValue=-5, reveal_pressed=True))
        studyCardsWidgets.btnNormal.clicked.connect(lambda: self.infoStudyCards(pValue=5, reveal_pressed=True, ))
        studyCardsWidgets.btnVeryGood.clicked.connect(lambda: self.infoStudyCards(pValue=10, reveal_pressed=True))
        studyCardsWidgets.btnRevealAnswer.setVisible(False)
        studyCardsWidgets.btnUnsatisfactory.setVisible(True)
        studyCardsWidgets.btnNormal.setVisible(True)
        studyCardsWidgets.btnVeryGood.setVisible(True)

if __name__ == "__main__":
    app = QApplication([])
    widget = FCardsMainPage()
    widget.show()
    sys.exit(app.exec_())
