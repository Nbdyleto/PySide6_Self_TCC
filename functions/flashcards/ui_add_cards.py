# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.
# to convert in this: python -m PyQt6.uic.pyuic -x addCards.ui -o ui_addCards

from PySide6 import QtCore, QtGui, QtWidgets

class Ui_AddCardsWindow(object):
    def setupUi(self, AddCardsWindow):
        AddCardsWindow.setObjectName("AddCardsWindow")
        AddCardsWindow.resize(405, 305)
        AddCardsWindow.setStyleSheet("""
    /*Window*/
        #AddCardsWindow {
            background-color: #282a36
        }
    /*QPushButton*/
        QPushButton {
            background-color: #6272a4;
            color: #282a36
        }
        QLabel {
            color: #f8f8f2
        }
        QPlainTextEdit {
            background-color: #44475a;
            selection-color: #6272a4;
            selection-background-color: #282a36
        }
        QListWidget {
            background-color: #44475a;
            color: #f8f8f2;
            selection-color: #282a36;
            selection-background-color: #ff79c6
        }
        """)
        

        self.centralwidget = QtWidgets.QWidget(AddCardsWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.pTextFront = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.pTextFront.setGeometry(QtCore.QRect(20, 70, 171, 141))
        self.pTextFront.setObjectName("pTextFront")
        self.pTextFront.setPlaceholderText("Put the front content here!")

        self.pTextVerse = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.pTextVerse.setGeometry(QtCore.QRect(210, 70, 171, 141))
        self.pTextVerse.setObjectName("pTextVerse")
        self.pTextVerse.setPlaceholderText("Put the verse content here!")

        self.btnAddCard = QtWidgets.QPushButton(self.centralwidget)
        self.btnAddCard.setGeometry(QtCore.QRect(190, 230, 88, 26))
        self.btnAddCard.setObjectName("btnAddCard")
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(290, 230, 88, 26))
        self.pushButton_2.setObjectName("pushButton_2")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(20, 10, 67, 18))
        self.label.setObjectName("label")
        self.pushButton_3 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_3.setGeometry(QtCore.QRect(370, 10, 31, 26))
        self.pushButton_3.setObjectName("pushButton_3")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(20, 50, 67, 18))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(210, 50, 67, 18))
        self.label_3.setObjectName("label_3")

        self.listDecks = QtWidgets.QListWidget(self.centralwidget)
        self.listDecks.setGeometry(QtCore.QRect(90, 10, 101, 41))
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
        self.btnAddCard.setText(_translate("AddCardsWindow", "Add"))
        self.pushButton_2.setText(_translate("AddCardsWindow", "Close"))
        self.label.setText(_translate("AddCardsWindow", "Add to..."))
        self.pushButton_3.setText(_translate("AddCardsWindow", "X"))
        self.label_2.setText(_translate("AddCardsWindow", "Front"))
        self.label_3.setText(_translate("AddCardsWindow", "Verse"))