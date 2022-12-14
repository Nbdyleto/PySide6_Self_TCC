# ///////////////////////////////////////////////////////////////
#
# BY: LEONARDO FERREIRA N. DA SILVA (WANDERSON M.PIMENTA)
# PROJECT MADE WITH: Qt Designer and PySide6
# V: 1.0.0
#
# This project can be used freely for all uses, as long as they maintain the
# respective credits only in the Python scripts, any information in the visual
# interface (GUI) can be modified without any implication.
#
# There are limitations on Qt licenses if you want to use your products
# commercially, I recommend reading them on the official website:
# https://doc.qt.io/qtforpython/licenses.html
#
# ///////////////////////////////////////////////////////////////

# MAIN FILE
# ///////////////////////////////////////////////////////////////
from main import *
from modules.app_settings import Settings

# WITH ACCESS TO MAIN WINDOW WIDGETS
# ///////////////////////////////////////////////////////////////
class AppFunctions(MainWindow):
    def setThemeBlue(self):
        Settings.BTN_LEFT_BOX_COLOR = "background-color: rgb(37, 37, 51);"
        Settings.BTN_RIGHT_BOX_COLOR = "background-color: rgb(37, 37, 51);"
        Settings.MENU_SELECTED_STYLESHEET = MENU_SELECTED_STYLESHEET = """
        border-left: 22px solid qlineargradient(spread:pad, x1:0.034, y1:0, x2:0.216, y2:0, stop:0.499 rgb(139, 136, 250), stop:0.5 rgb(37, 37, 51));
        background-color: rgb(37, 37, 51);
        """
        Settings.POMODORO_SELECTED_STYLESHEET = POMODORO_SELECTED_STYLESHEET = """
        background-color: rgb(139, 136, 250);
        """

        self.ui.textEdit.setHtml(QCoreApplication.translate("MainWindow", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><meta charset=\"utf-8\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:'Segoe UI'; font-size:10pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\" margin-top:12px; margin-bottom:12px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:12pt; font-weight:600; color:rgb(139, 136, 250);\">SELF</span></p>\n"
"<p align=\"center\" style=\" margin-top:12px; margin-bottom:12px; -qt-block-indent:0; text-indent:0px;\"><span style=\" color:#ffffff;\">Uma aplica????o criada com o objetivo de aumentar a produtividade e o foco nos estudos do usu??rio. Desenvolvida pelos crias da uni??o Embu da Serra.</span></p>\n"
"<p align=\"center\" style=\" margin-top:12px; margin-bottom:12px; -qt-block-indent:0; text-indent:0px;\"><span style=\" color:rgb(139, 136, 250);\">Jo??o Nogueira, Leonardo Ferreira, Lucas Tamarindo, Max Keven, Rodrigo Caldeira, Vinicius Saldanha </span></p>\n", None))

        #self.ui.home.setStyleSheet(u"background-image: url(:/images/images/images/SelfBlueLogo.png);\n"
#"background-position: center;\n"
#"background-repeat: no-repeat;")

    def setThemePurple(self):
        Settings.BTN_LEFT_BOX_COLOR = "background-color: rgb(45, 37, 51);"
        Settings.BTN_RIGHT_BOX_COLOR = "background-color: rgb(45, 37, 51);"
        Settings.MENU_SELECTED_STYLESHEET = MENU_SELECTED_STYLESHEET = """
        border-left: 22px solid qlineargradient(spread:pad, x1:0.034, y1:0, x2:0.216, y2:0, stop:0.499 rgb(194, 119, 250), stop:0.5 rgb(45, 37, 51));
        background-color: rgb(45, 37, 51);
        """
        Settings.POMODORO_SELECTED_STYLESHEET = POMODORO_SELECTED_STYLESHEET = """
        background-color: rgb(194, 119, 250);
        """

        self.ui.textEdit.setHtml(QCoreApplication.translate("MainWindow", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><meta charset=\"utf-8\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:'Segoe UI'; font-size:10pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\" margin-top:12px; margin-bottom:12px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:12pt; font-weight:600; color:rgb(194, 119, 250);\">SELF</span></p>\n"
"<p align=\"center\" style=\" margin-top:12px; margin-bottom:12px; -qt-block-indent:0; text-indent:0px;\"><span style=\" color:#ffffff;\">Uma aplica????o criada com o objetivo de aumentar a produtividade e o foco nos estudos do usu??rio. Desenvolvida pelos crias da uni??o Embu da Serra.</span></p>\n"
"<p align=\"center\" style=\" margin-top:12px; margin-bottom:12px; -qt-block-indent:0; text-indent:0px;\"><span style=\" color:rgb(194, 119, 250);\">Jo??o Nogueira, Leonardo Ferreira, Lucas Tamarindo, Max Keven, Rodrigo Caldeira, Vinicius Saldanha </span></p>\n", None))

        #self.ui.home.setStyleSheet(u"background-image: url(:/images/images/images/SelfPurpleLogo.png);\n"
#"background-position: center;\n"
#"background-repeat: no-repeat;")

    def setThemeGreen(self):
            Settings.BTN_LEFT_BOX_COLOR = "background-color: rgb(42, 48, 41);"
            Settings.BTN_RIGHT_BOX_COLOR = "background-color: rgb(42, 48, 41);"
            Settings.MENU_SELECTED_STYLESHEET = MENU_SELECTED_STYLESHEET = """
            border-left: 22px solid qlineargradient(spread:pad, x1:0.034, y1:0, x2:0.216, y2:0, stop:0.499 rgb(94, 171, 79), stop:0.5 rgb(42, 48, 41));
            background-color: rgb(42, 48, 41);
            """
            Settings.POMODORO_SELECTED_STYLESHEET = POMODORO_SELECTED_STYLESHEET = """
        background-color: rgb(94, 171, 79);
        """

            self.ui.textEdit.setHtml(QCoreApplication.translate("MainWindow", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
    "<html><head><meta name=\"qrichtext\" content=\"1\" /><meta charset=\"utf-8\" /><style type=\"text/css\">\n"
    "p, li { white-space: pre-wrap; }\n"
    "</style></head><body style=\" font-family:'Segoe UI'; font-size:10pt; font-weight:400; font-style:normal;\">\n"
    "<p align=\"center\" style=\" margin-top:12px; margin-bottom:12px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:12pt; font-weight:600; color:rgb(94, 171, 79);\">SELF</span></p>\n"
    "<p align=\"center\" style=\" margin-top:12px; margin-bottom:12px; -qt-block-indent:0; text-indent:0px;\"><span style=\" color:#ffffff;\">Uma aplica????o criada com o objetivo de aumentar a produtividade e o foco nos estudos do usu??rio. Desenvolvida pelos crias da uni??o Embu da Serra.</span></p>\n"
    "<p align=\"center\" style=\" margin-top:12px; margin-bottom:12px; -qt-block-indent:0; text-indent:0px;\"><span style=\" color:rgb(94, 171, 79);\">Jo??o Nogueira, Leonardo Ferreira, Lucas Tamarindo, Max Keven, Rodrigo Caldeira, Vinicius Saldanha </span></p>\n", None))

            #self.ui.home.setStyleSheet(u"background-image: url(:/images/images/images/SelfGreenLogo.png);\n"
    #"background-position: center;\n"
    #"background-repeat: no-repeat;")