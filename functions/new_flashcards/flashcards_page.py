import random
from PySide6 import QtCore, QtGui, QtWidgets
from functions.db_main_operations import DBMainOperations
from functions.new_flashcards.temp_ui_study import Ui_StudyCardsWindow
from functions.new_flashcards.ui_add_cards import Ui_addCardsWindow
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
        self.topicID = -1
        self.cardsTotal = 1
        self.studedCards = 1

    def setupConnections(self):
        # Main Page Connections
        widgets.btnAddDecks.clicked.connect(self.addNewDeck)
        widgets.classComboBox.currentIndexChanged.connect(self.selectTopicInComboBox)
        # Study Page Connections
        widgets.btnBackPage.clicked.connect(lambda: widgets.stackedWidget.setCurrentWidget(widgets.MainPage))
        widgets.btnBackPage.clicked.connect(self.resetPage)
        widgets.btnRevealAnswer.clicked.connect(self.revealAnswer)
        widgets.btnRevealAnswer.clicked.connect(lambda: widgets.btnRevealAnswer.setVisible(False))
        widgets.btnRevealAnswer.clicked.connect(lambda: widgets.btnBadFeedback.setVisible(True))
        widgets.btnRevealAnswer.clicked.connect(lambda: widgets.btnOkFeedback.setVisible(True))
        widgets.btnRevealAnswer.clicked.connect(lambda: widgets.btnGoodFeedback.setVisible(True))
        widgets.btnBadFeedback.clicked.connect(lambda: self.nextFlashcard(value=10))
        widgets.btnBadFeedback.clicked.connect(lambda: widgets.btnRevealAnswer.setVisible(True))
        widgets.btnOkFeedback.clicked.connect(lambda: self.nextFlashcard(value=40))
        widgets.btnOkFeedback.clicked.connect(lambda: widgets.btnRevealAnswer.setVisible(True))
        widgets.btnGoodFeedback.clicked.connect(lambda: self.nextFlashcard(value=60))
        widgets.btnGoodFeedback.clicked.connect(lambda: widgets.btnRevealAnswer.setVisible(True))
    
    def setupWidgets(self):
        widgets.stackedWidget.setCurrentIndex(1)
        widgets.btnBadFeedback.setVisible(False)
        widgets.btnOkFeedback.setVisible(False)
        widgets.btnGoodFeedback.setVisible(False)
        widgets.tblDecks.horizontalHeader().setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
        widgets.tblDecks.setColumnWidth(1,400)
        widgets.tblDecks.horizontalHeader().setSectionResizeMode(2, QtWidgets.QHeaderView.Stretch)
        widgets.tblDecks.horizontalHeader().setSectionResizeMode(3, QtWidgets.QHeaderView.Stretch)
        widgets.tblDecks.horizontalHeader().setSectionResizeMode(4, QtWidgets.QHeaderView.Stretch)
        widgets.tblDecks.horizontalHeader().setSectionResizeMode(5, QtWidgets.QHeaderView.Stretch)
        self.loadDecksInTable(showall=True, topicid=-1)
        self.loadTopicsInComboBox()
    
    def resetPage(self):
        self.studedCards = 1

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
            self.topicID = -1
            self.loadDecksInTable(showall=True, topicid=self.topicID)
        else:   # Show specific decks
            with DBMainOperations() as db:
                self.topicID = db.getAllRecords(tbl='topics', specifcols='topic_id', whclause=f'topic_name = "{topicname}"')[0][0]
            self.loadDecksInTable(showall=False, topicid=self.topicID)

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
            btnAction.clicked.connect(lambda: self.loadStudyInfo(deckid=deckid))
            btnAction.setToolTip('Iniciar estudos')
        else:
            btnAction.setObjectName(f'btnAddCards{tablerow}')
            btnAction.setStyleSheet(u"background-image: url(:/icons/images/icons/cil-plus.png);")
            btnAction.clicked.connect(lambda: self.openAddCardsWindow(deckid, deckname))
            btnAction.setToolTip('Adicionar cards')

        btnEditDecks = QtWidgets.QPushButton(widgets.tblDecks)
        btnEditDecks.setMinimumSize(QtCore.QSize(0, 100))
        btnEditDecks.setMaximumSize(QtCore.QSize(90, 16777215))
        btnEditDecks.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        btnEditDecks.setLayoutDirection(QtCore.Qt.LeftToRight)
        btnEditDecks.setObjectName(f'btnEditDecks{tablerow}')
        btnEditDecks.setStyleSheet(u"background-image: url(:/icons/images/icons/cil-pencil.png);")
        btnEditDecks.setToolTip('Editar deck')
        btnEditDecks.clicked.connect(lambda: self.editDeck(deckid))
        btnEditCards = QtWidgets.QPushButton(widgets.tblDecks)
        btnEditCards.setMinimumSize(QtCore.QSize(0, 100))
        btnEditCards.setMaximumSize(QtCore.QSize(90, 16777215))
        btnEditCards.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        btnEditCards.setLayoutDirection(QtCore.Qt.LeftToRight)
        btnEditCards.setObjectName(f'btnEditCards{tablerow}')
        btnEditCards.setToolTip('Editar cards')
        btnEditCards.setStyleSheet(u"background-image: url(:/icons/images/icons/cil-options.png);")
        btnRemoveDeck = QtWidgets.QPushButton(widgets.tblDecks)
        btnRemoveDeck.setMinimumSize(QtCore.QSize(0, 100))
        btnRemoveDeck.setMaximumSize(QtCore.QSize(90, 16777215))
        btnRemoveDeck.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        btnRemoveDeck.setLayoutDirection(QtCore.Qt.LeftToRight)
        btnRemoveDeck.setObjectName(f'btnRemoveDeck{tablerow}')
        btnRemoveDeck.setStyleSheet(u"background-image: url(:/icons/images/icons/cil-x-circle.png);")
        btnRemoveDeck.setToolTip('Remover deck')
        btnRemoveDeck.clicked.connect(lambda: self.removeDeck(deckid))

        widgets.tblDecks.setCellWidget(tablerow, 2, btnAction)
        widgets.tblDecks.setCellWidget(tablerow, 3, btnEditDecks)
        widgets.tblDecks.setCellWidget(tablerow, 4, btnEditCards)
        widgets.tblDecks.setCellWidget(tablerow, 5, btnRemoveDeck)

    def addNewDeck(self):
        newdeck, inputstatus = QtWidgets.QInputDialog.getText(self, "Novo Deck", "Entre com o nome do novo deck:")
        with DBMainOperations() as db:
            if inputstatus:
                qry = 'SELECT * FROM decks ORDER BY deck_id DESC LIMIT 1;'
                lastid = db.cursor.execute(qry).fetchall()[0][0]+1
                print('lastid:', lastid)
                db.populateTbl(tbl='decks', params=(lastid, newdeck, 0, self.topicID))
        self.loadDecksInTable(showall=False, topicid=self.topicID)
    
    def editDeck(self, deckid):
        newvalue, inputstatus = QtWidgets.QInputDialog.getText(self, "Alterar Nome", "Entre com o novo nome do deck:")
        with DBMainOperations() as db:
            if inputstatus:
                db.cursor.execute(f"UPDATE decks SET deck_name = '{newvalue}' WHERE deck_id == {deckid}")
        if self.topicID == -1:
            self.loadDecksInTable(showall=True, topicid=-1)
        else:
            self.loadDecksInTable(showall=False, topicid=self.topicID)

    def removeDeck(self, deckid):
        with DBMainOperations() as db:
            db.cursor.execute(f"DELETE from decks WHERE deck_id={deckid}")
        if self.topicID == -1:
            self.loadDecksInTable(showall=True, topicid=-1)
        else:
            self.loadDecksInTable(showall=False, topicid=self.topicID)

    ########################################
    # Study Cards Functions #####################################

    def loadStudyInfo(self, deckid):
        deckcols = 'deck_name, hits_percentage'
        cardcols = 'card_question, card_answer'
        with DBMainOperations() as db:
            deck = db.getAllRecords(tbl='decks', specifcols=(deckcols), whclause=f'deck_id={deckid}')
            deckcols = [col for col in deck[0]]
            deckname, deckperc = deckcols[0], deckcols[1]
            flashcards = db.getAllRecords(tbl='flashcards', specifcols=(cardcols), whclause=f'deck_id={deckid}')
            self.cardsTotal = len(flashcards)
            random.shuffle(flashcards)
            self.flashcardsIter = iter(flashcards)

        front, verse = next(self.flashcardsIter)
        widgets.textEditQuestion.setText(f'question: {front}')
        widgets.textEditAnswer.setText(f'answer: {verse}')
        widgets.textEditAnswer.setVisible(False)
        widgets.lblCardsCount.setText(f'{self.studedCards}/{self.cardsTotal}')
        widgets.lblDeckName.setText(deckname)
        widgets.progressBar.setValue(deckperc)
        widgets.stackedWidget.setCurrentWidget(widgets.StudyPage)

    def revealAnswer(self):
        widgets.textEditAnswer.setVisible(True)

    def nextFlashcard(self, value=0):
        self.studedCards += 1
        widgets.textEditAnswer.setVisible(False)
        widgets.btnRevealAnswer.setVisible(True)
        widgets.btnBadFeedback.setVisible(False)
        widgets.btnOkFeedback.setVisible(False)
        widgets.btnGoodFeedback.setVisible(False)
        try:
            front, verse = next(self.flashcardsIter)
            widgets.textEditQuestion.setText(f'question: {front}')
            widgets.textEditAnswer.setText(f'answer: {verse}')
            widgets.textEditAnswer.setVisible(False)
        except Exception:
            msgBox = QtWidgets.QMessageBox(self)
            msgBox.setText(f"Muito bem, estudo de deck finalizado!")
            msgBox.setInformativeText("Inicie, caso queira, um novo estudo de flashcards.") # later, put feedback, hints percentage etc.
            msgBox.show()
            widgets.btnBackPage.click()
        widgets.progressBar.setValue(value)
        widgets.lblCardsCount.setText(f'{self.studedCards}/{self.cardsTotal}')
        
    ########################################
    # AddCardsWindow Functions #####################################

    def openAddCardsWindow(self, deckid, deckname):
        self.addCardsWindow = QtWidgets.QMainWindow()
        self.ui_addCards = Ui_addCardsWindow()
        self.ui_addCards.setupUi(self.addCardsWindow)
        self.addCardsWindow.show()
        global widgetsAdd
        widgetsAdd = self.ui_addCards
        widgetsAdd.lblDeckName.setText(deckname)
        widgetsAdd.btnAddCardInDeck.clicked.connect(lambda: self.addCardsInDeck(deckid))
    
    def addCardsInDeck(self, deckid):
        front = widgetsAdd.plainTextEditFront.toPlainText()
        verse = widgetsAdd.plainTextEditVerse.toPlainText()
        if front and verse != "":
            with DBMainOperations() as db:
                lastid = db.cursor.execute('SELECT * FROM flashcards ORDER BY card_id DESC LIMIT 1;').fetchall()[0][0]+1
                db.populateTbl(tbl='flashcards', params=(lastid, front, verse, deckid))
                print(f'added: front: {front}, verse: {verse}')
                widgetsAdd.plainTextEditFront.clear()
                widgetsAdd.plainTextEditVerse.clear()
        else:
            retrymsg = QtWidgets.QMessageBox(self.addCardsWindow)
            retrymsg.setText('Coloque informações na carta! (frente e verso)')
            retrymsg.show()
        if self.topicID == -1:
            self.loadDecksInTable(showall=True, topicid=-1)
        else:
            self.loadDecksInTable(showall=False, topicid=self.topicID)