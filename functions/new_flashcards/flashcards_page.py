import random
from PySide6 import QtCore, QtGui, QtWidgets
from functions.db_main_operations import DBMainOperations
from functions.new_flashcards.temp_ui_add import Ui_AddCardsWindow # temp
from functions.new_flashcards.temp_ui_study import Ui_StudyCardsWindow # temp
from functions.new_flashcards.ui_flashcards_page import Ui_FlashcardsPage

class MainFlashcardsPage(QtWidgets.QWidget):
    def __init__(self):
        super(MainFlashcardsPage, self).__init__()
        self.ui = Ui_FlashcardsPage()
        self.ui.setupUi(self)
        self.setupVariables()
        self.setupConnections()
        self.setupWidgets()
    
    def setupVariables(self):
        global widgets
        widgets = self.ui
        self.flashcardsIter = None
        self.topicid = -1

    def setupConnections(self):
        # Main Page Connections
        widgets.btnAddDecks.clicked.connect(self.addNewDeck)
        widgets.classComboBox.currentIndexChanged.connect(self.selectTopicInComboBox)
        # Study Page Connections
        widgets.btnBackPage.clicked.connect(lambda: widgets.stackedWidget.setCurrentWidget(widgets.MainPage))
        widgets.btnBadFeedback.clicked.connect(self.nextFlashcard)
        widgets.btnOkFeedback.clicked.connect(self.nextFlashcard)
        widgets.btnGoodFeedback.clicked.connect(self.nextFlashcard)
    
    def setupWidgets(self):
        widgets.tblDecks.horizontalHeader().setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
        widgets.tblDecks.setColumnWidth(1,400)
        widgets.tblDecks.horizontalHeader().setSectionResizeMode(2, QtWidgets.QHeaderView.Stretch)
        widgets.tblDecks.horizontalHeader().setSectionResizeMode(3, QtWidgets.QHeaderView.Stretch)
        widgets.tblDecks.horizontalHeader().setSectionResizeMode(4, QtWidgets.QHeaderView.Stretch)
        widgets.tblDecks.horizontalHeader().setSectionResizeMode(5, QtWidgets.QHeaderView.Stretch)
        self.loadDecksInTable(showall=True, topicid=-1)
        self.loadTopicsInComboBox()

    def loadDecksInTable(self, showall=True, topicid=-1):
        if showall and topicid == -1:
            widgets.btnAddDecks.setDisabled(True)
            with DBMainOperations() as db:
                rowcount = db.getRowCount(tbl='decks')
                decks = db.getAllRecords(tbl='decks')
        else:
            widgets.btnAddDecks.setDisabled(False)
            with DBMainOperations() as db:
                rowcount = db.getRowCount(tbl='decks', whclause=f'topic_id = {topicid}')
                decks = db.getAllRecords(tbl='decks', whclause=f'topic_id = {topicid}')
        widgets.tblDecks.setRowCount(rowcount)
        widgets.tblDecks.clearContents()
        tablerow = 0
        for deck in decks:
            widgets.tblDecks.setRowHeight(tablerow, 100)
            widgets.tblDecks.setItem(tablerow, 0, QtWidgets.QTableWidgetItem(f'{str(deck[2])}%'))   #hints_percentage
            widgets.tblDecks.setItem(tablerow, 1, QtWidgets.QTableWidgetItem(deck[1]))  #deck_name
            self.loadWidgetsInRow(tablerow)
            tablerow+=1

        print(decks)

    def loadTopicsInComboBox(self):
        with DBMainOperations() as db:
            topics = db.getAllRecords(tbl='topics')
        tablerow = 0
        for row in topics:
            if row[0] == 0: # Ignore the first topic, that is empty.
                continue
            widgets.classComboBox.addItem(row[1])
            tablerow += 1

    def selectTopicInComboBox(self):
        idx = widgets.classComboBox.currentIndex()
        topicname = widgets.classComboBox.currentText()
        if idx == 0:    # Show geral
            self.topicid = -1
            self.loadDecksInTable(showall=True, topicid=self.topicid)
        else:   # Show specific decks
            with DBMainOperations() as db:
                self.topicid = db.getAllRecords(tbl='topics', specifcols='topic_id', whclause=f'topic_name = "{topicname}"')[0][0]
            self.loadDecksInTable(showall=False, topicid=self.topicid)

    def loadWidgetsInRow(self, tablerow):
        btnAction = QtWidgets.QPushButton(widgets.tblDecks)
        btnAction.setMinimumSize(QtCore.QSize(0, 100))
        btnAction.setMaximumSize(QtCore.QSize(90, 16777215))
        btnAction.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        btnAction.setLayoutDirection(QtCore.Qt.LeftToRight)
        with DBMainOperations() as db:
            deckname = widgets.tblDecks.item(tablerow, 1).text()
            deckid = db.getAllRecords(tbl='decks', specifcols='deck_id', whclause=f'deck_name = "{deckname}"')[0][0]
            hasflashcards = db.hasRecordsInTblFlashcards(id=deckid)
        if hasflashcards:
            btnAction.setObjectName(f'btnStartStudy{tablerow}')
            btnAction.setStyleSheet(u"background-image: url(:/icons/images/icons/cil-media-play.png);")
            btnAction.clicked.connect(lambda: self.loadStudyInfo(deckid))
        else:
            btnAction.setObjectName(f'btnAddCards{tablerow}')
            btnAction.setStyleSheet(u"background-image: url(:/icons/images/icons/cil-plus.png);")
            btnAction.clicked.connect(lambda: print('foo'))

        btnEditDecks = QtWidgets.QPushButton(widgets.tblDecks)
        btnEditDecks.setMinimumSize(QtCore.QSize(0, 100))
        btnEditDecks.setMaximumSize(QtCore.QSize(90, 16777215))
        btnEditDecks.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        btnEditDecks.setLayoutDirection(QtCore.Qt.LeftToRight)
        btnEditDecks.setObjectName(f'btnEditDecks{tablerow}')
        btnEditDecks.setStyleSheet(u"background-image: url(:/icons/images/icons/cil-pencil.png);")
        btnEditDecks.clicked.connect(lambda: self.editDeck(deckid))
        btnEditCards = QtWidgets.QPushButton(widgets.tblDecks)
        btnEditCards.setMinimumSize(QtCore.QSize(0, 100))
        btnEditCards.setMaximumSize(QtCore.QSize(90, 16777215))
        btnEditCards.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        btnEditCards.setLayoutDirection(QtCore.Qt.LeftToRight)
        btnEditCards.setObjectName(f'btnEditCards{tablerow}')
        btnEditCards.setStyleSheet(u"background-image: url(:/icons/images/icons/cil-options.png);")
        btnRemoveDeck = QtWidgets.QPushButton(widgets.tblDecks)
        btnRemoveDeck.setMinimumSize(QtCore.QSize(0, 100))
        btnRemoveDeck.setMaximumSize(QtCore.QSize(90, 16777215))
        btnRemoveDeck.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        btnRemoveDeck.setLayoutDirection(QtCore.Qt.LeftToRight)
        btnRemoveDeck.setObjectName(f'btnRemoveDeck{tablerow}')
        btnRemoveDeck.setStyleSheet(u"background-image: url(:/icons/images/icons/cil-x-circle.png);")

        widgets.tblDecks.setCellWidget(tablerow, 2, btnAction)
        widgets.tblDecks.setCellWidget(tablerow, 3, btnEditDecks)
        widgets.tblDecks.setCellWidget(tablerow, 4, btnEditCards)
        widgets.tblDecks.setCellWidget(tablerow, 5, btnRemoveDeck)

    def addNewDeck(self):
        newdeck, inputstatus = QtWidgets.QInputDialog.getText(self, "Novo Deck", "Entre com o nome do novo deck:")
        with DBMainOperations() as db:
            if inputstatus:
                lastid = db.getRowCount('decks')
                db.populateTbl(tbl='decks', params=(lastid, newdeck, 0, self.topicid))
        self.loadDecksInTable(showall=False, topicid=self.topicid)
    
    def editDeck(self, deckid):
        newvalue, inputstatus = QtWidgets.QInputDialog.getText(self, "Alterar Nome", "Entre com o novo nome do deck:")
        with DBMainOperations() as db:
            if inputstatus:
                db.cursor.execute(f"UPDATE decks SET deck_name = '{newvalue}' WHERE deck_id == {deckid}").fetchall()
        if self.topicid == -1:
            self.loadDecksInTable(showall=True, topicid=-1)
        else:
            self.loadDecksInTable(showall=False, topicid=self.topicid)
    # Study Cards Page

    def loadStudyInfo(self, deckid):
        deckcols = 'deck_name, hits_percentage'
        cardcols = 'card_question, card_answer'
        with DBMainOperations() as db:
            deck = db.getAllRecords(tbl='decks', specifcols=(deckcols), whclause=f'deck_id={deckid}')
            deckcols = [col for col in deck[0]]
            deckname, deckperc = deckcols[0], deckcols[1]
            flashcards = db.getAllRecords(tbl='flashcards', specifcols=(cardcols), whclause=f'deck_id={deckid}')
            cardstotal = len(flashcards)
            random.shuffle(flashcards)
            self.flashcardsIter = iter(flashcards)

        front, verse = next(self.flashcardsIter)
        widgets.textEdit.setText(f'question: {front}\nanswer: {verse}')
        widgets.lblCardsCount.setText(f'1/{cardstotal}')
        widgets.lblDeckName.setText(deckname)
        widgets.progressBar.setValue(deckperc)
        widgets.stackedWidget.setCurrentWidget(widgets.StudyPage)
    
    def nextFlashcard(self):
        try:
            front, verse = next(self.flashcardsIter)
            widgets.textEdit.setText(f'question: {front}\nanswer: {verse}')
        except Exception:
            self.flashcardsIter = None
        
    
        #widgets.textEdit.setText(next(flashcardsiter[0]))

        
    

    ######################################## Temporary Code Above!!!!!!!!!!!

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