import random
from PySide6 import QtCore, QtGui, QtWidgets
from functions.db_main_operations import DBMainOperations
from functions.json_operations import ImportExport
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
        self.deckID = -1
        self.cardsTotal = 1
        self.studedCards = 1

        # Study Progress:
        self.badEmojiCount, self.okEmojiCount, self.goodEmojiCount = 0, 0, 0
        self.hitsBadPercentage = 0
        self.hitsOkPercentage = 0
        self.hitsGoodPercentage = 0


    def setupConnections(self):
        # Main Page Connections
        widgets.btnAddDecks.clicked.connect(self.addNewDeck)
        widgets.classComboBox.currentIndexChanged.connect(self.selectTopicInComboBox)
        # Study Page Connections
        widgets.btnBackPage.clicked.connect(lambda: widgets.stackedWidget.setCurrentWidget(widgets.MainPage))
        widgets.btnBackPage.clicked.connect(lambda: widgets.stackedWidgetStudy.setCurrentWidget(widgets.studyListsPage))
        widgets.btnBackPage.clicked.connect(self.resetPage)
        widgets.btnRevealAnswer.clicked.connect(self.revealAnswer)
        widgets.btnRevealAnswer.clicked.connect(lambda: widgets.btnRevealAnswer.setVisible(False))
        widgets.btnRevealAnswer.clicked.connect(lambda: widgets.btnBadFeedback.setVisible(True))
        widgets.btnRevealAnswer.clicked.connect(lambda: widgets.btnOkFeedback.setVisible(True))
        widgets.btnRevealAnswer.clicked.connect(lambda: widgets.btnGoodFeedback.setVisible(True))
        widgets.btnBadFeedback.clicked.connect(lambda: self.nextFlashcard(emoji='bad'))
        widgets.btnBadFeedback.clicked.connect(lambda: widgets.btnRevealAnswer.setVisible(True))
        widgets.btnOkFeedback.clicked.connect(lambda: self.nextFlashcard(emoji='ok'))
        widgets.btnOkFeedback.clicked.connect(lambda: widgets.btnRevealAnswer.setVisible(True))
        widgets.btnGoodFeedback.clicked.connect(lambda: self.nextFlashcard(emoji='good'))
        widgets.btnGoodFeedback.clicked.connect(lambda: widgets.btnRevealAnswer.setVisible(True))
        # Edit Cards Page
        widgets.btnBackStudy.clicked.connect(lambda: widgets.stackedWidgetStudy.setCurrentWidget(widgets.studyListsPage))
        widgets.btnViewCards.clicked.connect(lambda: widgets.stackedWidgetStudy.setCurrentWidget(widgets.editCardsPage))
        widgets.btnViewCards.clicked.connect(self.loadCardsInTable)
        # Import/Export
        widgets.btnExport.clicked.connect(lambda: self.verifyTopicSelected())
        widgets.btnImport.clicked.connect(lambda: ImportExport.toSQLite3())
        widgets.btnImport.clicked.connect(lambda: self.loadDecksInTable())
        widgets.btnImport.clicked.connect(lambda: self.loadTopicsInComboBox())
    
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
        widgets.btnAddDecks.setToolTip('Adicionar deck')
        widgets.tblEditFlashcards.horizontalHeader().setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
        widgets.tblEditFlashcards.horizontalHeader().setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)
        widgets.tblEditFlashcards.horizontalHeader().setSectionResizeMode(2, QtWidgets.QHeaderView.Stretch)
    
    def resetPage(self):
        self.loadDecksInTable()
        self.studedCards = 1
        self.deckID = -1

    def verifyTopicSelected(self):
        # widgets.btnExport.clicked.connect(lambda: ImportExport.toJson(topicid=self.topicID))
        msgBox = QtWidgets.QMessageBox(self)
        if self.topicID == -1:
            msgBox.setText(f"Exportar tópico.")
            msgBox.setInformativeText("Selecione um tópico na barra para possibilitar sua exportação")
            msgBox.show()
        else:
            ImportExport.toJson(topicid=self.topicID)

    def loadDecksInTable(self, showall=True, topicid=-1):
        if showall and topicid == -1:
            with DBMainOperations() as db:
                rowcount = db.getRowCount(tbl='decks')
                decks = db.getAllRecords(tbl='decks')
        else:
            with DBMainOperations() as db:
                rowcount = db.getRowCount(tbl='decks', whclause=f'topic_id = {topicid}')
                decks = db.getAllRecords(tbl='decks', whclause=f'topic_id = {topicid}')
        widgets.tblDecks.setRowCount(rowcount)
        widgets.tblDecks.clearContents()
        tablerow = 0
        for deck in decks:
            widgets.tblDecks.setRowHeight(tablerow, 100)
            widgets.tblDecks.setItem(tablerow, 0, QtWidgets.QTableWidgetItem(f'{str(deck[2])}%'))   #hits_percentage
            widgets.tblDecks.setItem(tablerow, 1, QtWidgets.QTableWidgetItem(deck[1]))  #deck_name
            self.loadWidgetsInRow(tablerow)
            tablerow+=1

    def loadTopicsInComboBox(self):
        widgets.classComboBox.clear()
        with DBMainOperations() as db:
            topics = db.getAllRecords(tbl='topics')
        tablerow = 0
        for row in topics:
            if row[0] == 0:
                widgets.classComboBox.addItem('Geral')
                continue
            widgets.classComboBox.addItem(row[1])
            tablerow += 1
        widgets.classComboBox.addItem('Inserir novo tópico...')

    def selectTopicInComboBox(self):
        idx = widgets.classComboBox.currentIndex()
        self.topicName = widgets.classComboBox.currentText()
        topicname = self.topicName
        if idx == 0:    # Show geral
            self.topicID = -1
            self.loadDecksInTable(showall=True, topicid=self.topicID)
        elif idx == widgets.classComboBox.count()-1 and idx != -1: # Add topic
            self.topicID = -1
            self.addNewTopic()
        else:   # Show specific decks
            with DBMainOperations() as db:
                self.topicID = db.getAllRecords(tbl='topics', specifcols='topic_id', whclause=f'topic_name = "{topicname}"')[0][0]
            self.loadDecksInTable(showall=False, topicid=self.topicID)

    def addNewTopic(self):
        newtopic, inputstatus = QtWidgets.QInputDialog.getText(
            self, "Novo Tópico", "Entre com o nome do novo tópico:")
        with DBMainOperations() as db:
            if inputstatus:
                qry = 'SELECT * FROM topics ORDER BY topic_id DESC LIMIT 1;'
                lastid = db.cursor.execute(qry).fetchall()[0][0]+1
                db.populateTbl(tbl='topics', params=(lastid, newtopic))
                self.loadTopicsInComboBox()
                msgBox = QtWidgets.QMessageBox(self)
                msgBox.setText(f"O tópico '{newtopic}' foi adicionado!")
                msgBox.setInformativeText("Selecione-o e adicione novos decks.")
                msgBox.show()


    def loadWidgetsInRow(self, tablerow):
        btnAction = QtWidgets.QPushButton(widgets.tblDecks)
        btnAction.setMinimumSize(QtCore.QSize(0, 100))
        btnAction.setMaximumSize(QtCore.QSize(90, 16777215))
        btnAction.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        btnAction.setLayoutDirection(QtCore.Qt.LeftToRight)
        with DBMainOperations() as db:
            deckname = widgets.tblDecks.item(tablerow, 1).text()
            self.deckID = db.getAllRecords(tbl='decks', specifcols='deck_id', whclause=f'deck_name = "{deckname}"')[0][0]
            deckid = self.deckID
            hasflashcards = db.hasRecordsInTblFlashcards(id=deckid)
        if hasflashcards:
            btnAction.setObjectName(f'btnStartStudy{tablerow}')
            btnAction.setStyleSheet(u"""
            QPushButton{background-image: url(:/icons/images/icons/cil-media-play.png);}
            QToolTip{background-image: none;}
            """)
            btnAction.clicked.connect(lambda: self.loadStudyInfo(deckid=deckid))
            btnAction.setToolTip('Iniciar estudos')

        btnEditDecks = QtWidgets.QPushButton(widgets.tblDecks)
        btnEditDecks.setMinimumSize(QtCore.QSize(0, 100))
        btnEditDecks.setMaximumSize(QtCore.QSize(90, 16777215))
        btnEditDecks.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        btnEditDecks.setLayoutDirection(QtCore.Qt.LeftToRight)
        btnEditDecks.setObjectName(f'btnEditDecks{tablerow}')
        btnEditDecks.setStyleSheet(u"""
        QPushButton{background-image: url(:/icons/images/icons/cil-pencil.png);}
        QToolTip{background-image: none;}
        """)
        btnEditDecks.setToolTip('Editar deck')
        btnEditDecks.clicked.connect(lambda: self.editDeck(deckid))
        btnAddCards = QtWidgets.QPushButton(widgets.tblDecks)
        btnAddCards.setMinimumSize(QtCore.QSize(0, 100))
        btnAddCards.setMaximumSize(QtCore.QSize(90, 16777215))
        btnAddCards.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        btnAddCards.setLayoutDirection(QtCore.Qt.LeftToRight)
        btnAddCards.setObjectName(f'btnAddCards{tablerow}')
        btnAddCards.setToolTip('Adicionar cards')
        btnAddCards.setStyleSheet(u"""
        QPushButton{background-image: url(:/icons/images/icons/cil-library-add.png);}
        QToolTip{background-image: none;}
        """)
        btnAddCards.clicked.connect(lambda: self.openAddCardsWindow(deckid, deckname))
        btnRemoveDeck = QtWidgets.QPushButton(widgets.tblDecks)
        btnRemoveDeck.setMinimumSize(QtCore.QSize(0, 100))
        btnRemoveDeck.setMaximumSize(QtCore.QSize(90, 16777215))
        btnRemoveDeck.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        btnRemoveDeck.setLayoutDirection(QtCore.Qt.LeftToRight)
        btnRemoveDeck.setObjectName(f'btnRemoveDeck{tablerow}')
        btnRemoveDeck.setStyleSheet(u"""
        QPushButton{background-image: url(:/icons/images/icons/cil-x-circle.png);}
        QToolTip{background-image: none;}
        """)
        btnRemoveDeck.setToolTip('Remover deck')
        btnRemoveDeck.clicked.connect(lambda: self.removeDeck(deckid))

        widgets.tblDecks.setCellWidget(tablerow, 2, btnAction)
        widgets.tblDecks.setCellWidget(tablerow, 3, btnAddCards)
        widgets.tblDecks.setCellWidget(tablerow, 4, btnEditDecks)
        widgets.tblDecks.setCellWidget(tablerow, 5, btnRemoveDeck)

    def addNewDeck(self):
        if self.topicID == -1:
            msgBox = QtWidgets.QMessageBox(self)
            msgBox.setText(f"Adição de deck.")
            msgBox.setInformativeText("Selecione um tópico na barra para possibilitar a adição de um novo deck")
            msgBox.show()
        else:
            newdeck, inputstatus = QtWidgets.QInputDialog.getText(self, f"Novo Deck em {self.topicName}", "Entre com o nome do novo deck:")
            with DBMainOperations() as db:
                if inputstatus:
                    qry = 'SELECT * FROM decks ORDER BY deck_id DESC LIMIT 1;'
                    lastid = db.cursor.execute(qry).fetchall()[0][0]+1
                    db.populateTbl(tbl='decks', params=(lastid, newdeck, 0, 0, 0, 0, self.topicID))
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
        self.deckID = deckid
        self.loadCardsInTable()
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
        try:
            front, verse = next(self.flashcardsIter)
            widgets.textEditQuestion.setText(f'question: {front}')
            widgets.textEditAnswer.setText(f'answer: {verse}')
            widgets.textEditAnswer.setVisible(False)
            widgets.lblCardsCount.setText(f'{self.studedCards}/{self.cardsTotal}')
            widgets.lblDeckName.setText(deckname)
            widgets.progressBar.setValue(0)
            widgets.stackedWidget.setCurrentWidget(widgets.StudyPage)
        except: # If not exist cards.
            self.resetPage()
            widgets.stackedWidget.setCurrentWidget(widgets.MainPage)

    def revealAnswer(self):
        widgets.textEditAnswer.setVisible(True)

    def nextFlashcard(self, emoji=None):

        # Study Progress
        if emoji == "bad":
            self.badEmojiCount += 1
        elif emoji == "ok":
            self.okEmojiCount += 1
        elif emoji == "good":
            self.goodEmojiCount += 1
        else:
            pass
        
        self.hitsBadPercentage = (self.badEmojiCount/self.studedCards)*100
        self.hitsOkPercentage = (self.okEmojiCount/self.studedCards)*100
        self.hitsGoodPercentage = (self.goodEmojiCount/self.studedCards)*100

        print(self.hitsBadPercentage, "%, ", self.hitsOkPercentage, "%, ", self.hitsGoodPercentage, "%, ")

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
            msgBox.setInformativeText("Inicie, caso queira, um novo estudo de flashcards.") # later, put feedback, hits percentage etc.
            msgBox.show()
            self.updateEmojisCountInDB(deckid=self.deckID)
            widgets.btnBackPage.click()
            self.badEmojiCount, self.okEmojiCount, self.goodEmojiCount = 0, 0, 0
            self.hitsBadPercentage = 0
            self.hitsOkPercentage = 0
            self.hitsGoodPercentage = 0
        widgets.progressBar.setValue(self.hitsGoodPercentage + (self.hitsOkPercentage/2.3))
        widgets.lblCardsCount.setText(f'{self.studedCards}/{self.cardsTotal}')

    def updateEmojisCountInDB(self, deckid=-1):
        with DBMainOperations() as db:
            qry = f"""
                UPDATE decks SET bad_feedback = bad_feedback + {self.badEmojiCount}, 
                                 ok_feedback = ok_feedback + {self.okEmojiCount},
                                 good_feedback = good_feedback + {self.goodEmojiCount},
                                 hits_percentage = {round((self.hitsGoodPercentage + (self.hitsOkPercentage/2.3)), 2)}
                WHERE deck_id = {deckid} 
            """
            print(qry)
            db.cursor.execute(qry)
        
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

    ########################################
    # Edit Cards Functions #####################################

    def loadCardsInTable(self):
        widgets.tblEditFlashcards.clearContents()
        deckid = self.deckID
        try:
            with DBMainOperations() as db:
                cards = db.getAllRecords(tbl='flashcards', whclause=f'deck_id = {deckid}')
                widgets.tblEditFlashcards.setRowCount(len(cards))
            tablerow = 0
            for row in cards:
                widgets.tblEditFlashcards.setRowHeight(tablerow, 50)
                cardid, question, answer = row[0], row[1], row[2]
                btnRemoveCard = self.buttonToPutInRow(tablerow, cardid)
                widgets.tblEditFlashcards.setItem(tablerow, 0, QtWidgets.QTableWidgetItem(question))
                widgets.tblEditFlashcards.setItem(tablerow, 1, QtWidgets.QTableWidgetItem(answer))
                widgets.tblEditFlashcards.setCellWidget(tablerow, 2, btnRemoveCard)
                tablerow += 1 
            widgets.tblEditFlashcards.setRowHeight(tablerow, 50)
        except Exception as e:
            print('ERROR: ', e)

    def buttonToPutInRow(self, tablerow, cardid):
        btnRemoveCard = QtWidgets.QPushButton(widgets.tblEditFlashcards)
        btnRemoveCard.setMinimumSize(QtCore.QSize(0, 100))
        btnRemoveCard.setMaximumSize(QtCore.QSize(90, 16777215))
        btnRemoveCard.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        btnRemoveCard.setLayoutDirection(QtCore.Qt.LeftToRight)
        btnRemoveCard.setObjectName(f'btnRemoveCard{tablerow}')
        btnRemoveCard.setStyleSheet(u"""
            background-image: url(:/icons/images/icons/cil-x-circle.png);
            background-repeat: no-repeat;
            margin-top: 15px; 
            border-color: transparent;
        """)
        btnRemoveCard.clicked.connect(lambda: self.removeTask(cardid))
        btnRemoveCard.clicked.connect(lambda: self.loadStudyInfo(deckid=self.deckID))
        return btnRemoveCard

    def removeTask(self, cardid):
        with DBMainOperations() as db:
            db.cursor.execute(f"DELETE from flashcards WHERE card_id={cardid}")
        self.loadCardsInTable()
