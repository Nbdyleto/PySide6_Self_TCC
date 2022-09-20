import os
from pathlib import Path
import sys

from PySide6 import QtCore, QtGui, QtWidgets
from PySide6.QtWidgets import QWidget, QApplication

from .ui_flashcards_page import Ui_FlashcardsPage
from .ui_add_cards import Ui_AddCardsWindow
from .ui_study_cards import Ui_StudyCardsWindow

from ..db_main_operations import DBMainOperations

import json
import random

class FCardsMainPage(QWidget):
    def __init__(self):
        super(FCardsMainPage, self).__init__()
        self.ui = Ui_FlashcardsPage()
        self.ui.setupUi(self)

        global widgets
        widgets = self.ui

        self.addCardsWindow = None

        with DBMainOperations() as db:
            db.createTblTopics()
            db.createTblFlashcards()
            db.createTblTasks()
            db.popTblTopics((0, "Math", 0))
            db.popTblTopics((1, "Physics", 0))
            db.popTblTopics((2, "Chemistry", 0))
            db.popTblTopics((3, "TCC", 0))
            db.popTblFlashcards(("Quantos é 2+3?", "5", 0))
            db.popTblFlashcards(("Raiz quadrada de 7", "49", 0))
            db.popTblFlashcards(("Quantos é 9*7?", "63", 0))
        
        self.loadTopicsInTable()
        widgets.btnAddCards.clicked.connect(self.openAddCardsWindow)

        self.reveal_pressed = False
        self.studed_cards = 0
    
    # MainWindow Functions

    def loadTopicsInTable(self):
        with DBMainOperations() as db:
            rowcount = db.getRowCount(tbl='topics')
            topics = db.getAllRecords(tbl='topics')
        widgets.tblWidgetTopics.clearContents()
        widgets.tblWidgetTopics.setRowCount(rowcount+1)
        
        tablerow = 0
        for topic in topics:
            widgets.tblWidgetTopics.setRowHeight(tablerow, 50)
            widgets.tblWidgetTopics.setItem(tablerow, 0, QtWidgets.QTableWidgetItem(f'{str(topic[2])}%'))
            widgets.tblWidgetTopics.setItem(tablerow, 1, QtWidgets.QTableWidgetItem(topic[1]))
            self.loadWidgetCell(tablerow)
            tablerow+=1
            
        # last row of tblWidget has a 'add deck' option.
        lastrow = rowcount
        widgets.tblWidgetTopics.setRowHeight(tablerow, 50)
        widgets.tblWidgetTopics.setItem(lastrow, 1, QtWidgets.QTableWidgetItem('Create New Deck!'))
        btnAddDeck = QtWidgets.QPushButton(widgets.tblWidgetTopics)
        btnAddDeck.setText('+')
        widgets.tblWidgetTopics.setCellWidget(lastrow, 0, btnAddDeck)
        widgets.tblWidgetTopics.cellWidget(lastrow, 0).clicked.connect(self.addDeck)

    def loadWidgetCell(self, tablerow):
        btnStartStudy, btnAddCards = None, None
        with DBMainOperations() as db:
            print(db.hasRecordsInTblFlashcards(id=tablerow))
            if db.hasRecordsInTblFlashcards(id=tablerow):
                btnStartStudy = QtWidgets.QPushButton(widgets.tblWidgetTopics)
                btnStartStudy.setObjectName(f'btnStartStudy{tablerow}')
                btnStartStudy.setText('Start Study')
                widgets.tblWidgetTopics.setCellWidget(tablerow, 2, btnStartStudy)
                btnStartStudy.clicked.connect(lambda: self.openStudyCardsWindow(row_clicked=tablerow))
            else:
                btnAddCards = QtWidgets.QPushButton(widgets.tblWidgetTopics)
                btnAddCards.setObjectName(f'btnAddCards{tablerow}')
                btnAddCards.setText('Add Cards')
                widgets.tblWidgetTopics.setCellWidget(tablerow, 2, btnAddCards)
                btnAddCards.clicked.connect(lambda: self.openAddCardsWindow(row_clicked=tablerow))
    
    @QtCore.Slot()
    def addDeck(self):
        new_topic, input_status = QInputDialog.getText(self, "New Topic", "Enter The Name of Topic:")
        if input_status:
            row = (self.rowcount, new_topic, 0)
        with DBMainOperations() as db:
            qry_insert = "INSERT INTO topics (topic_id, topic_name, hits_percentage) VALUES (?,?,?);"
            db.populate(qry_insert, row)
            self.loadTopicsInTable()

    # AddCardsWindow Functions #####################################
    
    @QtCore.Slot()
    def openAddCardsWindow(self, row_clicked):
        self.addCardsWindow = QtWidgets.QMainWindow()
        self.ui_addCards = Ui_AddCardsWindow()
        self.ui_addCards.setupUi(self.addCardsWindow)

        global cardsWinWidgets
        cardsWinWidgets = self.ui_addCards
        
        lbl_active_topic = QtWidgets.QLabel(self.addCardsWindow)
        lbl_active_topic.setGeometry(QtCore.QRect(270, 20, 90, 20))
        with DBMainOperations() as db:
            topic_name = db.getAllRecords(tbl='topics', specifcols='topic_name')[0][0]
        lbl_active_topic.setText(topic_name)

        cardsWinWidgets.listTopics.setCurrentRow(0)
        self.addCardsWindow.show()
        cardsWinWidgets.btnAddCard.clicked.connect(self.addCards)

        self.loadTopicsList()
    
    def loadTopicsList(self):
        with DBMainOperations() as db:
            topics = db.getAllRecords(tbl='topics', specifcols='topic_name', fetchall=True)
        print(topics)
        for topic_name in topics:
            cardsWinWidgets.listTopics.addItem(topic_name[0])

    @QtCore.Slot()
    def addCards(self):
        card_question = cardsWinWidgets.pTextFront.toPlainText()
        card_answer = cardsWinWidgets.pTextVerse.toPlainText()
        if card_question and card_answer != "":
            topic_id = cardsWinWidgets.listTopics.currentRow()
            card_question = cardsWinWidgets.pTextFront.toPlainText()
            card_answer = cardsWinWidgets.pTextVerse.toPlainText()
            with DBMainOperations() as db:
                print('populating...')
                db.popTblFlashcards(params=(card_question, card_answer, topic_id))
            self.winAddCardsClearContents()
            self.loadTopicsInTable()
        else:
            retry_msg = QtWidgets.QMessageBox(self.addCardsWindow)
            retry_msg.setStyleSheet("color: black")
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
        self.cardIterator = None
        self.infoStudyCards(topic_id=row_clicked)

        self.studyCardsWindow.show()

    def infoStudyCardsWindow(self, row_clicked):
        with DBMainOperations() as db:
            records = db.getAllRecords(tbl='topics', specifcols='hits_percentage, topic_name', 
                                       fetchall=True, whclause=f'topic_id={row_clicked}')
            self.total_cards = db.getRowCount(tbl='flashcards')
        hits_percentage = records[0][0]
        studyCardsWidgets.pBarHitsPercentage.setValue(hits_percentage)
        topic_name = records[0][1]
        studyCardsWidgets.lblDeckName.setText(topic_name)
        
    def infoStudyCards(self, reveal_pressed=False, topic_id=None):
        if reveal_pressed:
            self.studed_cards += 1
        studyCardsWidgets.btnRevealAnswer.setVisible(True)
        studyCardsWidgets.btnUnsatisfactory.setVisible(False)
        studyCardsWidgets.btnNormal.setVisible(False)
        studyCardsWidgets.btnVeryGood.setVisible(False)

        if self.cardIterator is None:
            # Create a cardIterator if no exists (always the studyCards page is called).
            self.studed_cards = 1
            with DBMainOperations() as db:
                cards = db.getAllRecords(tbl='flashcards', specifcols='card_question, card_answer',
                                         fetchall=True, whclause=f'topic_id = {topic_id}')
            random.shuffle(cards)
            self.cardIterator = iter(cards)

        try:
            front, verse = next(self.cardIterator)
            studyCardsWidgets.plainTextEdit.setPlainText(front)
            studyCardsWidgets.btnRevealAnswer.clicked.connect(lambda: self.revealCardAnswer(verse))
            studyCardsWidgets.lblCardsQnt.setText(f"{self.studed_cards}/{str(self.total_cards)}")
        except:
            if self.studed_cards > self.total_cards:
                self.studyCardsWindow.close()
            print('Stop Iteration')

    def revealCardAnswer(self, verse):
        studyCardsWidgets.plainTextEdit.setPlainText(verse)
        studyCardsWidgets.btnUnsatisfactory.clicked.connect(lambda: self.infoStudyCards(reveal_pressed=True))
        studyCardsWidgets.btnNormal.clicked.connect(lambda: self.infoStudyCards(reveal_pressed=True))
        studyCardsWidgets.btnVeryGood.clicked.connect(lambda: self.infoStudyCards(reveal_pressed=True))
        studyCardsWidgets.btnRevealAnswer.setVisible(False)
        studyCardsWidgets.btnUnsatisfactory.setVisible(True)
        studyCardsWidgets.btnNormal.setVisible(True)
        studyCardsWidgets.btnVeryGood.setVisible(True)

if __name__ == "__main__":
    app = QApplication([])
    widget = FCardsMainPage()
    widget.show()
    sys.exit(app.exec_())
