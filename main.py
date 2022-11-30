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
            db.populateTbl(tbl='topics', params=(1, "Enem"))
            db.populateTbl(tbl='topics', params=(2, "Fuvest"))

            ################# FLASHCARDS

            db.populateTbl(tbl='decks', params=(0, "Enem Humanas", 67.3, 10, 3, 5, 1))
            db.populateTbl(tbl='decks', params=(1, "Enem Exatas", 77.4, 12, 7, 10, 1))
            db.populateTbl(tbl='decks', params=(2, "Fuvest Humanas", 59.1, 5, 10, 5, 2))
            db.populateTbl(tbl='decks', params=(3, "Fuvest Exatas", 70.5, 5, 3, 6, 2))

            db.populateTbl(tbl='flashcards', params=(0, "Antitese pode ser classificada como?", "Uma figura de linguagem", 0))
            db.populateTbl(tbl='flashcards', params=(1, "Quem foi a pessoa que sancionou a Lei Áurea?", "Princesa Isabel", 0))
            db.populateTbl(tbl='flashcards', params=(2, "Qual a principal caracteristica do estoicismo?", "o pensamento de que todo o cosmos é regido por uma harmonia que determina todos os acontecimentos.", 0))
            db.populateTbl(tbl='flashcards', params=(3, 
                """A caixa-d’água de um edifício terá a forma de um paralelepípedo retângulo reto 
                com volume igual a 28 080 litros. Em uma maquete que representa o edifício, a caixa-d’água tem 
                dimensões 2 cm × 3,51 cm × 4 cm. Dado: 1 dm³ = 1 L, A escala usada pelo arquiteto foi: """, "1 : 100", 1))
            db.populateTbl(tbl='flashcards', params=(4, "Qual o uso adequado da hiperbole?", "Ela é utilizada para passar uma ideia de intensidade por meio de expressões exageradas intencionalmente", 3))
            db.populateTbl(tbl='flashcards', params=(5, "uais paises faziam parte dos aliados na segunda guerra mundial?", "Os aliados eram Estados Unidos, Inglaterra, França e União sovietica.", 2))
            db.populateTbl(tbl='flashcards', params=(6, "Diferencie acidos e bases", "Um ácido será toda espécie química que sobre ionização liberando como único cátion o H+ em meio aquoso. Já as bases, sofrem dissociação liberando como único ânion o OH-", 3))
            db.populateTbl(tbl='flashcards', params=(7, "Qual a função da mitocondria?", "As mitocôndrias são organelas celulares relacionadas com o processo de respiração celular", 1))

            ################# TASKS

            db.populateTbl(tbl='tasks', params=(0, 'Resolver simulado do ENEM 2019', 'Em Progresso...', '2022-11-24', 
                               '2022-11-24', 1))
            db.populateTbl(tbl='tasks', params=(1, 'Resolução de exercícios envolvendo parábola.', 'Finalizada!', '2022-11-24', 
                               '2022-11-29', 1))
            db.populateTbl(tbl='tasks', params=(2, 'Estudo e análise de problemas matemáticos', 'Finalizada!', '2022-11-26', 
                               '2022-11-30', 0))
            db.populateTbl(tbl='tasks', params=(3, 'Estudo, utilizando pomodoro, envolvendo Biologia Celular', 'Não Iniciada...', '2022-11-29', 
                               '2022-11-30', 1))
            db.populateTbl(tbl='tasks', params=(4, 'Realizar uma redação com o tema do ENEM 2022', 'Não Iniciada.', '2022-11-02', 
                               '2022-11-24', 1))
            db.populateTbl(tbl='tasks', params=(5, 'Elaborar uma redação que envolva os conteúdos estudados', 'Não Iniciada.', '2022-11-24', 
                               '2022-11-24', 2))
            db.populateTbl(tbl='tasks', params=(6, 'Estudo, utilizando pomodoro, envolvendo Redes', 'Não Iniciada...', '2022-11-29', 
                               '2022-11-30', 0))
            #db.populateTbl('tasks', params=(0, 'Apresentar TCC', 'Em Progresso...', '2022-10-24', '2022-10-25', 4))
            #db.populateTbl('tasks', params=(1, 'Resolver questões de matemática', 'Não Iniciada.', '2022-10-22', '2022-10-25', 1))
            #db.populateTbl('tasks', params=(2, 'Resolver questões sobre genética', 'Não Iniciada.', '2022-10-22', '2022-10-22', 3))
            #db.populateTbl('tasks', params=(3, 'Desenvolver funcionalidade Pomodoro', 'Em Progresso...', '2022-10-20', '2022-10-27', 4))
            #db.populateTbl('tasks', params=(4, 'Fazer Simulado do ENEM 2020', 'Não Iniciada.', '2022-10-20', '2022-10-25', 0))

            ################### POMODORO
            db.populateTbl(tbl='pomodoroProgress', params=(0, True, '25-05-2022', '00:25:00', 2))
            db.populateTbl(tbl='pomodoroProgress', params=(1, True, '25-05-2022', '00:25:00', 2))
            db.populateTbl(tbl='pomodoroProgress', params=(2, True, '25-05-2022', '00:25:00', 2))
            db.populateTbl(tbl='pomodoroProgress', params=(3, True, '25-05-2022', '00:24:30', 2))
            db.populateTbl(tbl='pomodoroProgress', params=(4, True, '25-05-2022', '00:25:00', 1))
            db.populateTbl(tbl='pomodoroProgress', params=(5, True, '25-05-2022', '00:21:20', 1))
            db.populateTbl(tbl='pomodoroProgress', params=(6, True, '25-05-2022', '00:25:20', 1))
            db.populateTbl(tbl='pomodoroProgress', params=(7, True, '25-05-2022', '00:25:00', 1))
            db.populateTbl(tbl='pomodoroProgress', params=(8, True, '25-05-2022', '00:22:00', 1))
            db.populateTbl(tbl='pomodoroProgress', params=(9, True, '25-05-2022', '00:35:00', 1))
            db.populateTbl(tbl='pomodoroProgress', params=(10, True, '25-05-2022', '00:25:00', 1))
            db.populateTbl(tbl='pomodoroProgress', params=(11, True, '25-05-2022', '00:25:00', 2))
            db.populateTbl(tbl='pomodoroProgress', params=(12, True, '25-05-2022', '00:22:00', 1))
            db.populateTbl(tbl='pomodoroProgress', params=(13, True, '25-05-2022', '00:35:00', 1))
            db.populateTbl(tbl='pomodoroProgress', params=(14, True, '25-05-2022', '00:25:00', 2))
            db.populateTbl(tbl='pomodoroProgress', params=(15, True, '25-05-2022', '00:25:00', 1))
            db.populateTbl(tbl='pomodoroProgress', params=(16, True, '25-05-2022', '00:22:00', 2))
            db.populateTbl(tbl='pomodoroProgress', params=(17, True, '25-05-2022', '00:35:00', 2))
            db.populateTbl(tbl='pomodoroProgress', params=(18, True, '25-05-2022', '00:25:00', 1))

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
        self.setUserChangePallete(True)
        widgets.btnPyJucoPurple.clicked.connect(lambda: self.setUserChangePallete(True))
        widgets.btnPyJucoPurple.clicked.connect(self.changePallete)
        widgets.btnPyJucoBlue.clicked.connect(lambda: self.setUserChangePallete(True))
        widgets.btnPyJucoBlue.clicked.connect(self.changePallete)
        widgets.btnPyJucoGreen.clicked.connect(lambda: self.setUserChangePallete(True))
        widgets.btnPyJucoGreen.clicked.connect(self.changePallete)
        widgets.newPomodoroPage.ui.btnPomodoro.clicked.connect(lambda: self.setUserChangePallete(False))
        widgets.newPomodoroPage.ui.btnPomodoro.clicked.connect(self.changePallete)
        widgets.newPomodoroPage.ui.btnShortRest.clicked.connect(lambda: self.setUserChangePallete(False))
        widgets.newPomodoroPage.ui.btnShortRest.clicked.connect(self.changePallete)
        widgets.newPomodoroPage.ui.btnLongRest.clicked.connect(lambda: self.setUserChangePallete(False))
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
            widgets.seeProgressPage.setupFlashcardsStats()
            widgets.seeProgressPage.setupPomodoroStats()

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
            widgets.newPomodoroPage.loadTopicsInList()

        # SHOW DAILY TASK PAGE
        if btnName == "btn_daily_task_page":
            widgets.stackedWidget.setCurrentWidget(widgets.newDailyTaskPage) # SET PAGE
            UIFunctions.resetStyle(self, btnName) # RESET ANOTHERS BUTTONS SELECTED
            self.btnSelected.setStyleSheet(UIFunctions.selectMenu(self.btnSelected.styleSheet()))
            widgets.newDailyTaskPage.loadDataInTable()
            widgets.newDailyTaskPage.hideAll()

        # PRINT BTN NAME
        print(f'Button "{btnName}" pressed!')

    def setUserChangePallete(self, value=False):
        self.userChange = value

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
            if not self.userChange: # change color of button selected just in pomodoro, not in pallete menus. 
                UIFunctions.resetButtonsStyle(self, btn.objectName()) # RESET ANOTHERS POMODORO BUTTONS
                btn.setStyleSheet(UIFunctions.selectButton(btn.styleSheet())) # SET SELECTED POMODORO BUTTON
            else:
                print('nao vo mudar, pois self.userChange: ', self.userChange)
                UIFunctions.resetButtonsStyle(self, btn.objectName())

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
