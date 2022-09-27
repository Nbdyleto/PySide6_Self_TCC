# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.
# to convert in this: python -m PyQt6.uic.pyuic -x addCards.ui -o ui_addCards

from PySide6 import QtCore, QtGui, QtWidgets

class Ui_AddCardsWindow(object):
    def setupUi(self, AddCardsWindow):
        AddCardsWindow.setObjectName("AddCardsWindow")
        AddCardsWindow.resize(405, 405)
    
        self.centralwidget = QtWidgets.QWidget(AddCardsWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.pTextFront = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.pTextFront.setGeometry(QtCore.QRect(20, 150, 171, 141))
        self.pTextFront.setObjectName("pTextFront")
        self.pTextFront.setPlaceholderText("Put the front content here!")

        self.pTextVerse = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.pTextVerse.setGeometry(QtCore.QRect(210, 150, 171, 141))
        self.pTextVerse.setObjectName("pTextVerse")
        self.pTextVerse.setPlaceholderText("Put the verse content here!")

        self.btnAddCard = QtWidgets.QPushButton(self.centralwidget)
        self.btnAddCard.setGeometry(QtCore.QRect(180, 310, 100, 26))
        self.btnAddCard.setObjectName("btnAddCard")
        self.btnClose = QtWidgets.QPushButton(self.centralwidget)
        self.btnClose.setGeometry(QtCore.QRect(290, 310, 88, 26))
        self.btnClose.setObjectName("btnClose")
        self.lblAddTo = QtWidgets.QLabel(self.centralwidget)
        self.lblAddTo.setGeometry(QtCore.QRect(20, 10, 100, 18))
        self.lblAddTo.setObjectName("lblAddTo")
        self.pushButton_3 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_3.setGeometry(QtCore.QRect(370, 10, 31, 26))
        self.pushButton_3.setObjectName("pushButton_3")
        self.lblFront = QtWidgets.QLabel(self.centralwidget)
        self.lblFront.setGeometry(QtCore.QRect(20, 125, 67, 18))
        self.lblFront.setObjectName("lblFront")
        self.lblVerse = QtWidgets.QLabel(self.centralwidget)
        self.lblVerse.setGeometry(QtCore.QRect(210, 125, 67, 18))
        self.lblVerse.setObjectName("lblVerse")

        self.listDecks = QtWidgets.QListWidget(self.centralwidget)
        self.listDecks.setGeometry(QtCore.QRect(130, 10, 125, 100))
        self.listDecks.setObjectName("listDecks")
        self.listDecks.setCurrentRow(2)

        AddCardsWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(AddCardsWindow)
        self.statusbar.setObjectName("statusbar")
        AddCardsWindow.setStatusBar(self.statusbar)

        self.retranslateUi(AddCardsWindow)
        QtCore.QMetaObject.connectSlotsByName(AddCardsWindow)

    def retranslateUi(self, AddCardsWindow):
        _translate = QtCore.QCoreApplication.translate
        AddCardsWindow.setWindowTitle(_translate("AddCardsWindow", "AddCardsWindow"))
        self.btnAddCard.setText(_translate("AddCardsWindow", "Adicionar"))
        self.btnClose.setText(_translate("AddCardsWindow", "Fechar"))
        self.lblAddTo.setText(_translate("AddCardsWindow", "Adicionar a..."))
        self.pushButton_3.setText(_translate("AddCardsWindow", "X"))
        self.lblFront.setText(_translate("AddCardsWindow", "Frente"))
        self.lblVerse.setText(_translate("AddCardsWindow", "Verso"))