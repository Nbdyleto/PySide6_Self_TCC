# ///////////////////////////////////////////////////////////////
#
# BY: WANDERSON M.PIMENTA (AND MODIFIED BY LEONARDO FERREIRA)
# PROJECT MADE WITH: Qt Designer and PySide6
# V: 1.0.0
#
# ///////////////////////////////////////////////////////////////

import sys
import os
import platform

from functions.db_main_operations import DBMainOperations
from functions.flashcards.json_operations import ImportExport

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

            db.populateTbl(tbl='flashcards', params=("Quantos é 2+3?", "5", 0))
            db.populateTbl(tbl='flashcards', params=("Raiz quadrada de 7", "49", 0))
            db.populateTbl(tbl='flashcards', params=("Quantos é 9*7?", "63", 0))
            
            db.populateTbl(tbl='flashcards', params=("Qual o maior osso humano?", "Fêmur", 1))
            db.populateTbl(tbl='flashcards', params=("Quantos ossos possuem o ser humano?", "206", 1))

            db.populateTbl(tbl='flashcards', params=("Qual é a primeira lei de Newton?", "Princípio da Inércia", 3))
            db.populateTbl(tbl='flashcards', params=("No que consiste a primeira lei?", "Um objeto em repouso ou movimento retilíneo uniforme tende a permanecer nesse estado se a força resultante sobre ele é nula.", 3))

            ################# TASKS

            # query_insert = f"INSERT INTO tasks(task_name, status, start_date, end_date, topic_id) VALUES (?,?,?,?,?)"
            db.populateTbl('tasks', params=('Apresentar TCC', 'Em Progresso', '2022-10-24', '2022-10-25', 4))
            db.populateTbl('tasks', params=('Resolver questões de matemática', 'Não iniciada', '2022-10-22', '2022-10-25', 1))
            db.populateTbl('tasks', params=('Resolver questões sobre genética', 'Não iniciada', '2022-10-22', '2022-10-22', 3))
            db.populateTbl('tasks', params=('Desenvolver funcionalidade Pomodoro', 'Em Progresso', '2022-10-20', '2022-10-27', 4))
            db.populateTbl('tasks', params=('Fazer Simulado do ENEM 2020', 'Não iniciada', '2022-10-20', '2022-10-25', 0))

            import_export = ImportExport()
            import_export._to_json(topic_id=1)

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
        widgets.btnPyJucoPurple.clicked.connect(self.buttonClick)
        widgets.btnPyJucoBlue.clicked.connect(self.buttonClick)
        widgets.btnPyJucoGreen.clicked.connect(self.buttonClick)

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
        btn = self.sender()
        btnName = btn.objectName()

        # SHOW HOME PAGE
        if btnName == "btn_home":
            widgets.stackedWidget.setCurrentWidget(widgets.home)
            UIFunctions.resetStyle(self, btnName)
            btn.setStyleSheet(UIFunctions.selectMenu(btn.styleSheet()))

        # SHOW WIDGETS PAGE
        if btnName == "btn_progress_page":
            widgets.stackedWidget.setCurrentWidget(widgets.widgets)
            UIFunctions.resetStyle(self, btnName)
            btn.setStyleSheet(UIFunctions.selectMenu(btn.styleSheet()))

        # SHOW FLASHCARDS PAGE
        if btnName == "btn_flashcards_page":
            widgets.stackedWidget.setCurrentWidget(widgets.testNewCardsPage) # SET PAGE
            UIFunctions.resetStyle(self, btnName) # RESET ANOTHERS BUTTONS SELECTED
            btn.setStyleSheet(UIFunctions.selectMenu(btn.styleSheet())) # SELECT MENU

        if btnName == "btn_pomodoro_page":
            widgets.stackedWidget.setCurrentWidget(widgets.pomodoroPage) # SET PAGE
            UIFunctions.resetStyle(self, btnName) # RESET ANOTHERS BUTTONS SELECTED
            btn.setStyleSheet(UIFunctions.selectMenu(btn.styleSheet())) # SELECT MENU
            widgets.pomodoroPage.load_data_in_table()

        # SHOW DAILY TASK PAGE
        if btnName == "btn_daily_task_page":
            widgets.stackedWidget.setCurrentWidget(widgets.newDailyTaskPage) # SET PAGE
            UIFunctions.resetStyle(self, btnName) # RESET ANOTHERS BUTTONS SELECTED
            btn.setStyleSheet(UIFunctions.selectMenu(btn.styleSheet())) # SELECT MENU
            widgets.dailyTaskPage.load_data_in_table()

        if btnName == "btnPyJucoPurple":
            UIFunctions.theme(self, self.purpleFile, True)
            AppFunctions.setThemePurple(self)
        if btnName == "btnPyJucoBlue":
            UIFunctions.theme(self, self.blueFile, True)
            AppFunctions.setThemeBlue(self)
        if btnName == "btnPyJucoGreen":
            UIFunctions.theme(self, self.greenFile, True)
            AppFunctions.setThemeGreen(self)

        # PRINT BTN NAME
        print(f'Button "{btnName}" pressed!')


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
