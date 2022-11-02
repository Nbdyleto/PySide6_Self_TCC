# ///////////////////////////////////////////////////////////////
#
# BY: WANDERSON M.PIMENTA
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

# WITH ACCESS TO MAIN WINDOW WIDGETS
# ///////////////////////////////////////////////////////////////
class AppFunctions(MainWindow):
    def setThemeHack(self):
        Settings.BTN_LEFT_BOX_COLOR = "background-color: rgb(42, 48, 41);"
        Settings.BTN_RIGHT_BOX_COLOR = "background-color: rgb(42, 48, 41);"
        Settings.MENU_SELECTED_STYLESHEET = MENU_SELECTED_STYLESHEET = """
        border-left: 22px solid qlineargradient(spread:pad, x1:0.034, y1:0, x2:0.216, y2:0, stop:0.499 rgb(94, 171, 79), stop:0.5 rgb(42, 48, 41));
        background-color: rgb(42, 48, 41);
        """

        # SET MANUAL STYLES
        self.ui.lineEdit.setStyleSheet("background-color: #6272a4;")
        self.ui.pushButton.setStyleSheet("background-color: #6272a4;")
        self.ui.plainTextEdit.setStyleSheet("background-color: #6272a4;")
        self.ui.tableWidget.setStyleSheet("QScrollBar:vertical { background: #6272a4; } QScrollBar:horizontal { background: #6272a4; }")
        self.ui.scrollArea.setStyleSheet("QScrollBar:vertical { background: #6272a4; } QScrollBar:horizontal { background: #6272a4; }")
        self.ui.comboBox.setStyleSheet("background-color: #6272a4;")
        self.ui.horizontalScrollBar.setStyleSheet("background-color: #6272a4;")
        self.ui.verticalScrollBar.setStyleSheet("background-color: #6272a4;")
        self.ui.commandLinkButton.setStyleSheet("color: #ff79c6;")

    def setThemeBlue(self):
        Settings.BTN_LEFT_BOX_COLOR = "background-color: rgb(37, 37, 51);"
        Settings.BTN_RIGHT_BOX_COLOR = "background-color: rgb(37, 37, 51);"
        Settings.MENU_SELECTED_STYLESHEET = MENU_SELECTED_STYLESHEET = """
        border-left: 22px solid qlineargradient(spread:pad, x1:0.034, y1:0, x2:0.216, y2:0, stop:0.499 rgb(139, 136, 250), stop:0.5 rgb(37, 37, 51));
        background-color: rgb(37, 37, 51);
        """

        self.ui.textEdit.setHtml(QCoreApplication.translate("MainWindow", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><meta charset=\"utf-8\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:'Segoe UI'; font-size:10pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\" margin-top:12px; margin-bottom:12px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:12pt; font-weight:600; color:rgb(139, 136, 250);\">SELF</span></p>\n"
"<p align=\"center\" style=\" margin-top:12px; margin-bottom:12px; -qt-block-indent:0; text-indent:0px;\"><span style=\" color:#ffffff;\">Uma aplicação criada com o objetivo de aumentar a produtividade e o foco nos estudos do usuário. Desenvolvida pelos crias da união Embu da Serra.</span></p>\n"
"<p align=\"center\" style=\" margin-top:12px; margin-bottom:12px; -qt-block-indent:0; text-indent:0px;\"><span style=\" color:rgb(139, 136, 250);\">João Nogueira, Leonardo Ferreira, Lucas Tamarindo, Max Keven, Rodrigo Caldeira, Vinicius Saldanha </span></p>\n", None))

    def setThemePurple(self):
        Settings.BTN_LEFT_BOX_COLOR = "background-color: rgb(45, 37, 51);"
        Settings.BTN_RIGHT_BOX_COLOR = "background-color: rgb(45, 37, 51);"
        Settings.MENU_SELECTED_STYLESHEET = MENU_SELECTED_STYLESHEET = """
        border-left: 22px solid qlineargradient(spread:pad, x1:0.034, y1:0, x2:0.216, y2:0, stop:0.499 rgb(194, 119, 250), stop:0.5 rgb(45, 37, 51));
        background-color: rgb(45, 37, 51);
        """

        self.ui.textEdit.setHtml(QCoreApplication.translate("MainWindow", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><meta charset=\"utf-8\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:'Segoe UI'; font-size:10pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\" margin-top:12px; margin-bottom:12px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:12pt; font-weight:600; color:rgb(194, 119, 250);\">SELF</span></p>\n"
"<p align=\"center\" style=\" margin-top:12px; margin-bottom:12px; -qt-block-indent:0; text-indent:0px;\"><span style=\" color:#ffffff;\">Uma aplicação criada com o objetivo de aumentar a produtividade e o foco nos estudos do usuário. Desenvolvida pelos crias da união Embu da Serra.</span></p>\n"
"<p align=\"center\" style=\" margin-top:12px; margin-bottom:12px; -qt-block-indent:0; text-indent:0px;\"><span style=\" color:rgb(194, 119, 250);\">João Nogueira, Leonardo Ferreira, Lucas Tamarindo, Max Keven, Rodrigo Caldeira, Vinicius Saldanha </span></p>\n", None))
