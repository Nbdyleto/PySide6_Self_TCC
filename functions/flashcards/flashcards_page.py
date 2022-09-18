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

        self.studyCardsWindow.show()

    def loadWindowInfo(self, rowClicked):
        hitsPercentage, topicName = self.getTopicInfo(rowClicked)
        studyCardsWidgets.lblDeckName.setText(topicName)

        cardsRecords, cardsCount = self.getFlashcardsInfo(rowClicked)
        studyCardsWidgets.lblCardsQnt.setText(f"1/{str(cardsCount)}")

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
            cardsCount = (db.cursor.execute(qry).fetchone())[0]

        return cardsRecords, cardsCount

    #######################

    # JSON CONVERT FUNCTIONS
    
    def _to_json(self):
        """Convert a sqlite3 database to json"""
        with FlashcardsDB() as db:
            results = db.cursor.execute("SELECT * from topics")
            rows = [row for row in results]
            cols = [col for col in results.description]
 
        topics = []
        for row in rows:
            topic = {}
            for col_name, val in zip(cols, row):
                topic[col_name] = val
            topics.append(row)
            
        with open('topics.json', 'w') as json_file:
            topicsJSON = json.dumps(topics, indent=4)
            print(f"topics in JSON: {topicsJSON}")
            json.dump(topicsJSON, json_file)

if __name__ == "__main__":
    app = QApplication([])
    widget = FCardsMainPage()
    widget.show()
    sys.exit(app.exec_())
