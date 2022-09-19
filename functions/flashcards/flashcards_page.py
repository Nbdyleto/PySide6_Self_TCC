import os
from pathlib import Path
import sys

from PySide6 import QtCore, QtGui, QtWidgets
from PySide6.QtWidgets import QWidget, QApplication

from .ui_flashcards_page import Ui_FlashcardsPage
from .db_flashcards_operations import FlashcardsDB
from .ui_add_cards import Ui_AddCardsWindow
from .ui_study_cards import Ui_StudyCardsWindow

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

        with FlashcardsDB() as db:
            db.create_table()
        
        self.loadTopicsInTable()
        widgets.btnAddCards.clicked.connect(self.openAddCardsWindow)

        self._to_json()

        self.revealpressed = False
        self.cardsqnt = 0
    
    # MainWindow Functions

    def loadTopicsInTable(self):
        with FlashcardsDB() as db:
            rowCount = (db.cursor.execute("SELECT COUNT(*) FROM topics").fetchone())[0]
            topics = db.cursor.execute("SELECT * FROM topics").fetchall()

        self.rowCount = rowCount+1
        widgets.tblWidgetTopics.clearContents()
        widgets.tblWidgetTopics.setRowCount(self.rowCount)
        
        tablerow = 0
        print(topics)
        for topic in topics:
            widgets.tblWidgetTopics.setRowHeight(tablerow, 60)
            widgets.tblWidgetTopics.setItem(tablerow, 0, QtWidgets.QTableWidgetItem(f'{str(topic[2])}%'))
            widgets.tblWidgetTopics.setItem(tablerow, 1, QtWidgets.QTableWidgetItem(topic[1]))
            self.loadWidgetCell(tablerow)
            tablerow+=1
            
        lastrow = self.rowCount-1
        widgets.tblWidgetTopics.setRowHeight(tablerow, 60)
        widgets.tblWidgetTopics.setItem(lastrow, 1, QtWidgets.QTableWidgetItem('Create New Deck!'))
        btnCell = QtWidgets.QPushButton(widgets.tblWidgetTopics)
        btnCell.setText('+')
        widgets.tblWidgetTopics.setCellWidget(lastrow, 0, btnCell)
        widgets.tblWidgetTopics.cellWidget(lastrow, 0).clicked.connect(self.addDeck)

        print("="*50)

    def loadWidgetCell(self, tablerow):
        btnStartStudy, btnAddCards = None, None
        hasRecordsInDB = self.hasRecordsInDB(tablerow)
        with FlashcardsDB() as db:
            if hasRecordsInDB:
                results = db.cursor.execute(f"SELECT * FROM flashcards WHERE (topic_id = {tablerow})")
                rows = [row for row in results]
                print(rows)
                
                btnStartStudy = QtWidgets.QPushButton(widgets.tblWidgetTopics)
                btnStartStudy.setObjectName(f'btnStudyRow{tablerow}')
                btnStartStudy.setText('Start Study')
                widgets.tblWidgetTopics.setCellWidget(tablerow, 2, btnStartStudy)
                btnStartStudy.clicked.connect(lambda: self.openStudyCardsWindow(rowClicked=tablerow))
            else:
                btnAddCards = QtWidgets.QPushButton(widgets.tblWidgetTopics)
                print('NOT EXISTS')
                btnAddCards.setText('Add Cards')
                btnAddCards.setObjectName(f'btnAddCards{tablerow}')
                widgets.tblWidgetTopics.setCellWidget(tablerow, 2, btnAddCards)
                btnAddCards.clicked.connect(lambda: self.openAddCardsWindow(rowClicked=tablerow))

    def hasRecordsInDB(self, tablerow): 
        with FlashcardsDB() as db:
            qry = f"SELECT COUNT(*) FROM flashcards WHERE (topic_id = {tablerow})"
            recordCount = db.cursor.execute(qry).fetchall()[0][0]
            if recordCount > 0:
                return True
            return False

    @QtCore.Slot()
    def addDeck(self):
        new_topic, input_status = QInputDialog.getText(self, "New Topic", "Enter The Name of Topic:")
        if input_status:
            row = (self.rowCount, new_topic, 0)
        with FlashcardsDB() as db:
            qry_insert = "INSERT INTO topics (topic_id, topic_name, hits_percentage) VALUES (?,?,?);"
            db.populate(qry_insert, row)
            self.loadTopicsInTable()

    # AddCardsWindow Functions #####################################

    @QtCore.Slot()
    def openAddCardsWindow(self, rowClicked):
        self.addCardsWindow = QtWidgets.QMainWindow()
        self.ui_addCards = Ui_AddCardsWindow()
        self.ui_addCards.setupUi(self.addCardsWindow)

        global cardsWinWidgets
        cardsWinWidgets = self.ui_addCards
        
        lblActiveTopic = QtWidgets.QLabel(self.addCardsWindow)
        lblActiveTopic.setGeometry(QtCore.QRect(270, 20, 90, 20))
        hitsPercentage, topicName = self.getTopicInfo(rowClicked)
        lblActiveTopic.setText(topicName)

        cardsWinWidgets.listTopics.setCurrentRow(0)
        self.addCardsWindow.show()
        cardsWinWidgets.btnAddCard.clicked.connect(self.addCards)

        self.loadTopicsList()
    
    def loadTopicsList(self):
        with FlashcardsDB() as db:
            qry_select = "SELECT (topic_name) from topics"
            topics = db.cursor.execute(qry_select).fetchall()
        print(topics)
        for topic in topics:
            cardsWinWidgets.listTopics.addItem(topic[0])

    @QtCore.Slot()
    def addCards(self):
        card_question = cardsWinWidgets.pTextFront.toPlainText()
        card_answer = cardsWinWidgets.pTextVerse.toPlainText()
        if card_question and card_answer != "":
            topic_id = cardsWinWidgets.listTopics.currentRow()
            card_question = cardsWinWidgets.pTextFront.toPlainText()
            card_answer = cardsWinWidgets.pTextVerse.toPlainText()
            qry_insert = "INSERT INTO flashcards VALUES (?,?,?)"
            row = (card_question, card_answer, topic_id)
            with FlashcardsDB() as db:
                print('populating...')
                db.populate(qry_insert, row)
            self.addCardsClearContents()
            self.loadTopicsInTable()
        else:
            retry_msg = QtWidgets.QMessageBox(self.addCardsWindow)
            retry_msg.setStyleSheet("color: black")
            retry_msg.setText('Input something in your card (front and verse)!')
            retry_msg.show()

    def addCardsClearContents(self):
        cardsWinWidgets.pTextFront.clear()
        cardsWinWidgets.pTextVerse.clear()

    # StudyCards Functions #################################

    @QtCore.Slot()
    def openStudyCardsWindow(self, rowClicked):
        self.studyCardsWindow = QtWidgets.QMainWindow()
        self.ui_studyCards = Ui_StudyCardsWindow()
        self.ui_studyCards.setupUi(self.studyCardsWindow)

        global studyCardsWidgets
        studyCardsWidgets = self.ui_studyCards

        self.loadWindowInfo(rowClicked)
        self.cardIterator = None
        self.loadCardsInfo(rowClicked)

        self.studyCardsWindow.show()

    def loadCardsInfo(self, rowClicked=None):
        if self.revealpressed:
            self.cardsqnt += 1
        self.revealpressed = False

        studyCardsWidgets.btnRevealAnswer.setVisible(True)
        studyCardsWidgets.btnUnsatisfactory.setVisible(False)
        studyCardsWidgets.btnNormal.setVisible(False)
        studyCardsWidgets.btnVeryGood.setVisible(False)

        if self.cardIterator is None:
            # Create a cardIterator if is None (always the studyCards page is called).
            self.cardsqnt = 1
            with FlashcardsDB() as db:
                qry = f"SELECT card_question, card_answer from flashcards WHERE topic_id == ?"
                cards = db.cursor.execute(qry, (rowClicked,)).fetchall()
            random.shuffle(cards)
            self.cardIterator = iter(cards)

        try:
            front, verse = next(self.cardIterator)
            print(front, verse)
            studyCardsWidgets.plainTextEdit.setPlainText(front)
            studyCardsWidgets.btnRevealAnswer.clicked.connect(lambda: self.revealCardAnswer(verse))
            studyCardsWidgets.lblCardsQnt.setText(f"{self.cardsqnt}/{str(self.cardscount)}")
        except:
            if self.cardsqnt > self.cardscount:
                self.studyCardsWindow.close()
            print('Stop Iteration')

    def revealCardAnswer(self, verse):
        self.revealpressed = True

        studyCardsWidgets.plainTextEdit.setPlainText(verse)
        studyCardsWidgets.btnUnsatisfactory.clicked.connect(lambda: self.loadCardsInfo())
        studyCardsWidgets.btnNormal.clicked.connect(lambda: self.loadCardsInfo())
        studyCardsWidgets.btnVeryGood.clicked.connect(lambda: self.loadCardsInfo())
        studyCardsWidgets.btnRevealAnswer.setVisible(False)
        studyCardsWidgets.btnUnsatisfactory.setVisible(True)
        studyCardsWidgets.btnNormal.setVisible(True)
        studyCardsWidgets.btnVeryGood.setVisible(True)

    def loadWindowInfo(self, rowClicked):
        hitsPercentage, topicName = self.getTopicInfo(rowClicked)
        studyCardsWidgets.lblDeckName.setText(topicName)

        cardsRecords, self.cardscount = self.getFlashcardsInfo(rowClicked)
        studyCardsWidgets.pBarHitsPercentage.setValue(hitsPercentage)

    def getTopicInfo(self, topic_id):
        with FlashcardsDB() as db:
            qry = f"SELECT hits_percentage, topic_name FROM topics WHERE topic_id == {topic_id}"
            results = db.cursor.execute(qry).fetchall()
            hitsPercentage = results[0][0]
            topicName = results[0][1]
        return hitsPercentage, topicName

    def getFlashcardsInfo(self, topic_id):
        with FlashcardsDB() as db:
            qry = f"SELECT * FROM flashcards WHERE topic_id == {topic_id}"
            cardsRecords = db.cursor.execute(qry).fetchall()

            qry = f"SELECT COUNT(*) FROM flashcards WHERE topic_id == {topic_id}"
            cardscount = (db.cursor.execute(qry).fetchone())[0]

        return cardsRecords, cardscount

if __name__ == "__main__":
    app = QApplication([])
    widget = FCardsMainPage()
    widget.show()
    sys.exit(app.exec_())
