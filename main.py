# ///////////////////////////////////////////////////////////////
#
# BY: WANDERSON M.PIMENTA (AND MODIFIED BY LEONARDO FERREIRA)
# PROJECT MADE WITH: Qt Designer and PySide6
# V: 1.0.0
#
# ///////////////////////////////////////////////////////////////

import modules.resources_rc as resources_rc
import sys
import os
import platform

from functions.db_main_operations import DBMainOperations

# IMPORT / GUI AND MODULES AND WIDGETS
# ///////////////////////////////////////////////////////////////
from modules import *
from widgets import *
os.environ["QT_FONT_DPI"] = "96" # FIX Problem for High DPI and Scale above 100%

# SET AS GLOBAL WIDGETS
# ///////////////////////////////////////////////////////////////
widgets = None

class MainWindow(QMainWindow):
    def __init__(self):

        with DBMainOperations() as db:
            db.createTblTopics()
            db.createTblTasks()
            db.createTblDecks()
            db.createTblFlashcards()
            db.createTblPomodoroProgress()

            ################# TOPICS

            db.populateTbl(tbl='topics', params=(0, ""))
            db.populateTbl(tbl='topics', params=(1, "Matemática"))
            db.populateTbl(tbl='topics', params=(2, "Física"))
            db.populateTbl(tbl='topics', params=(3, "Química"))
            db.populateTbl(tbl='topics', params=(4, "TCC"))

            ################# FLASHCARDS

            db.populateTbl(tbl='decks', params=(0, "Cálculos Básicos", 0 , 1))
            db.populateTbl(tbl='decks', params=(1, "Genética", 0, 3))
            db.populateTbl(tbl='decks', params=(2, "Polaridade", 0, 3))
            db.populateTbl(tbl='decks', params=(3, "Leis de Newton", 0, 2))

            db.populateTbl(tbl='flashcards', params=(0, "Quantos é 2+3?", "5", 0))
            db.populateTbl(tbl='flashcards', params=(1, "Raiz quadrada de 7", "49", 0))
            db.populateTbl(tbl='flashcards', params=(2, "Quantos é 9*7?", "63", 0))
            
            db.populateTbl(tbl='flashcards', params=(3, "Qual o maior osso humano?", "Fêmur", 1))
            db.populateTbl(tbl='flashcards', params=(4, "Quantos ossos possuem o ser humano?", "206", 1))

            db.populateTbl(tbl='flashcards', params=(5, "Qual é a primeira lei de Newton?", "Princípio da Inércia", 3))
            db.populateTbl(tbl='flashcards', params=(6, "No que consiste a primeira lei?", "Um objeto em repouso ou movimento retilíneo uniforme tende a permanecer nesse estado se a força resultante sobre ele é nula.", 3))

            ################# TASKS

            db.populateTbl('tasks', params=(0, 'Apresentar TCC', 'Em Progresso...', '2022-10-24', '2022-10-25', 4))
            db.populateTbl('tasks', params=(1, 'Resolver questões de matemática', 'Não Iniciada.', '2022-10-22', '2022-10-25', 1))
            db.populateTbl('tasks', params=(2, 'Resolver questões sobre genética', 'Não Iniciada.', '2022-10-22', '2022-10-22', 3))
            db.populateTbl('tasks', params=(3, 'Desenvolver funcionalidade Pomodoro', 'Em Progresso...', '2022-10-20', '2022-10-27', 4))
            db.populateTbl('tasks', params=(4, 'Fazer Simulado do ENEM 2020', 'Não Iniciada.', '2022-10-20', '2022-10-25', 0))

        QMainWindow.__init__(self)

        # SET AS GLOBAL WIDGETS
        # ///////////////////////////////////////////////////////////////
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        global widgets
        widgets = self.ui

        # USE CUSTOM TITLE BAR | USE AS "False" FOR MAC OR LINUX
        # ///////////////////////////////////////////////////////////////
        Settings.ENABLE_CUSTOM_TITLE_BAR = True

        # APP NAME
        # ///////////////////////////////////////////////////////////////
        title = "SELF - Produtividade e Foco"
        description = "SELF - Seu Estudo com Liberdade e Fundamento"
        # APPLY TEXTS
        self.setWindowTitle(title)
        widgets.titleRightInfo.setText(description)

        # TOGGLE MENU
        # ///////////////////////////////////////////////////////////////
        widgets.toggleButton.clicked.connect(lambda: UIFunctions.toggleMenu(self, True))

        # SET UI DEFINITIONS
        # ///////////////////////////////////////////////////////////////
        UIFunctions.uiDefinitions(self)

        # QTableWidget PARAMETERS
        # ///////////////////////////////////////////////////////////////
        widgets.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        # BUTTONS CLICK
        # ///////////////////////////////////////////////////////////////

        # LEFT MENUS
        widgets.btn_home.clicked.connect(self.buttonClick)
        widgets.btn_progress_page.clicked.connect(self.buttonClick)
        widgets.btn_flashcards_page.clicked.connect(self.buttonClick)
        widgets.btn_pomodoro_page.clicked.connect(self.buttonClick)
        widgets.btn_daily_task_page.clicked.connect(self.buttonClick)

        # PALLETE BUTTONS
        widgets.btnPyJucoPurple.clicked.connect(self.changePallete)
        widgets.btnPyJucoBlue.clicked.connect(self.changePallete)
        widgets.btnPyJucoGreen.clicked.connect(self.changePallete)
        widgets.newPomodoroPage.ui.btnPomodoro.clicked.connect(self.changePallete)
        widgets.newPomodoroPage.ui.btnShortRest.clicked.connect(self.changePallete)
        widgets.newPomodoroPage.ui.btnLongRest.clicked.connect(self.changePallete)
        
        # EXTRA LEFT BOX
        def openCloseLeftBox():
            UIFunctions.toggleLeftBox(self, True)
        widgets.toggleLeftBox.clicked.connect(openCloseLeftBox)
        widgets.extraCloseColumnBtn.clicked.connect(openCloseLeftBox)

        # EXTRA RIGHT BOX
        def openCloseRightBox():
            UIFunctions.toggleRightBox(self, True)
        widgets.settingsTopBtn.clicked.connect(openCloseRightBox)

        # SHOW APP
        # ///////////////////////////////////////////////////////////////
        self.show()

        self.purpleFile = "themes/pyjuco_purple.qss"
        self.blueFile = "themes/pyjuco_blue.qss"
        self.greenFile = "themes/pyjuco_green.qss"
        ### SET DEFAULT THEME
        UIFunctions.theme(self, self.purpleFile, True)
        AppFunctions.setThemePurple(self)

        # SET HOME PAGE AND SELECT MENU
        # ///////////////////////////////////////////////////////////////
        widgets.stackedWidget.setCurrentWidget(widgets.home)
        widgets.btn_home.setStyleSheet(UIFunctions.selectMenu(widgets.btn_home.styleSheet()))

    # BUTTONS CLICK
    # Post here your functions for clicked buttons
    # ///////////////////////////////////////////////////////////////
    def buttonClick(self):
        # GET BUTTON CLICKED
        self.btnSelected = self.sender()
        btnName = self.btnSelected.objectName()

        # SHOW HOME PAGE
        if btnName == "btn_home":
            widgets.stackedWidget.setCurrentWidget(widgets.home)
            UIFunctions.resetStyle(self, btnName)
            self.btnSelected.setStyleSheet(UIFunctions.selectMenu(self.btnSelected.styleSheet()))

        # SHOW WIDGETS PAGE
        if btnName == "btn_progress_page":
            widgets.stackedWidget.setCurrentWidget(widgets.seeProgressPage)
            UIFunctions.resetStyle(self, btnName)
            self.btnSelected.setStyleSheet(UIFunctions.selectMenu(self.btnSelected.styleSheet()))
            #widgets.newPomodoroPage.updateTimeInDB()
            #widgets.seeProgressPage.getTotalTime()
            widgets.seeProgressPage.loadTopicsInComboBox()
            widgets.seeProgressPage.setupStatsInWidgets()

        # SHOW FLASHCARDS PAGE
        if btnName == "btn_flashcards_page":
            widgets.stackedWidget.setCurrentWidget(widgets.newFlashcardsPage) # SET PAGE
            UIFunctions.resetStyle(self, btnName) # RESET ANOTHERS BUTTONS SELECTED
            self.btnSelected.setStyleSheet(UIFunctions.selectMenu(self.btnSelected.styleSheet()))
            widgets.newFlashcardsPage.loadTopicsInComboBox()

        if btnName == "btn_pomodoro_page":
            widgets.stackedWidget.setCurrentWidget(widgets.newPomodoroPage) # SET PAGE
            UIFunctions.resetStyle(self, btnName) # RESET ANOTHERS BUTTONS SELECTED
            self.btnSelected.setStyleSheet(UIFunctions.selectMenu(self.btnSelected.styleSheet())) 
            widgets.newPomodoroPage.loadDataInTable()

        # SHOW DAILY TASK PAGE
        if btnName == "btn_daily_task_page":
            widgets.stackedWidget.setCurrentWidget(widgets.newDailyTaskPage) # SET PAGE
            UIFunctions.resetStyle(self, btnName) # RESET ANOTHERS BUTTONS SELECTED
            self.btnSelected.setStyleSheet(UIFunctions.selectMenu(self.btnSelected.styleSheet()))
            widgets.newDailyTaskPage.loadDataInTable()
            widgets.newDailyTaskPage.hideAll()

        # PRINT BTN NAME
        print(f'Button "{btnName}" pressed!')

    def changePallete(self):
        if widgets.newPomodoroPage.allowChangeModeManually:

            btn = self.sender()
            btnName = btn.objectName()

            UIFunctions.resetButtonsStyle(self, widget=None, resetall=True) # RESET ALL MENU BUTTONS SELECTED
            UIFunctions.resetStyle(self, widget=None, resetall=True)    # RESET ALL POMODORO BUTTONS SELECTED

            if btnName == "btnPomodoro" or btnName == "btnPyJucoBlue":
                UIFunctions.theme(self, self.blueFile, True)
                AppFunctions.setThemeBlue(self)
            if btnName == "btnShortRest" or btnName == "btnPyJucoGreen":
                UIFunctions.theme(self, self.greenFile, True)
                AppFunctions.setThemeGreen(self)
            if btnName == "btnLongRest" or btnName == "btnPyJucoPurple":
                UIFunctions.theme(self, self.purpleFile, True)
                AppFunctions.setThemePurple(self)

            UIFunctions.resetStyle(self, self.btnSelected.objectName()) # RESET ANOTHERS MENU BUTTONS
            self.btnSelected.setStyleSheet(UIFunctions.selectMenu(self.btnSelected.styleSheet())) # SET SELECTED MENU BUTTON
            UIFunctions.resetButtonsStyle(self, btn.objectName()) # RESET ANOTHERS POMODORO BUTTONS
            btn.setStyleSheet(UIFunctions.selectButton(btn.styleSheet())) # SET SELECTED POMODORO BUTTON

    # RESIZE EVENTS
    # ///////////////////////////////////////////////////////////////
    def resizeEvent(self, event):
        # Update Size Grips
        UIFunctions.resize_grips(self)

    # MOUSE CLICK EVENTS
    # ///////////////////////////////////////////////////////////////
    def mousePressEvent(self, event):
        # SET DRAG POS WINDOW
        self.dragPos = event.globalPos()

        # PRINT MOUSE EVENTS
        if event.buttons() == Qt.LeftButton:
            print('Mouse click: LEFT CLICK')
        if event.buttons() == Qt.RightButton:
            print('Mouse click: RIGHT CLICK')

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon("icon.ico"))
    window = MainWindow()
    sys.exit(app.exec_())
