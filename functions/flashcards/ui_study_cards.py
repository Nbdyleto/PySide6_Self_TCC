# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.
# to convert in this: python -m PyQt6.uic.pyuic -x addCards.ui -o ui_addCards

from PySide6 import QtCore, QtGui, QtWidgets

class Ui_StudyCardsWindow(object):
    def setupUi(self, StudyCardsWindow):
        StudyCardsWindow.setObjectName("StudyCardsWindow")
        StudyCardsWindow.resize(308, 387)

        self.centralwidget = QtWidgets.QWidget(StudyCardsWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.plainTextEdit = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.plainTextEdit.setGeometry(QtCore.QRect(30, 92, 251, 221))
        self.plainTextEdit.setObjectName("plainTextEdit")

        self.btnRevealAnswer = QtWidgets.QPushButton(self.centralwidget)
        self.btnRevealAnswer.setGeometry(QtCore.QRect(30, 317, 251, 31))
        self.btnRevealAnswer.setObjectName("btnRevealAnswer")

        self.btnUnsatisfactory = QtWidgets.QPushButton(self.centralwidget)
        self.btnUnsatisfactory.setGeometry(QtCore.QRect(100, 317, 31, 31))
        self.btnUnsatisfactory.setObjectName("btnUnsatisfactory")

        self.btnNormal = QtWidgets.QPushButton(self.centralwidget)
        self.btnNormal.setGeometry(QtCore.QRect(140, 317, 31, 31))
        self.btnNormal.setObjectName("btnNormal")

        self.btnVeryGood = QtWidgets.QPushButton(self.centralwidget)
        self.btnVeryGood.setGeometry(QtCore.QRect(180, 317, 31, 31))
        self.btnVeryGood.setObjectName("btnVeryGood")
        
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(30, 57, 41, 18))
        self.label.setObjectName("label")
        self.lblDeckName = QtWidgets.QLabel(self.centralwidget)
        self.lblDeckName.setGeometry(QtCore.QRect(80, 57, 101, 18))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lblDeckName.sizePolicy().hasHeightForWidth())
        self.lblDeckName.setSizePolicy(sizePolicy)
        self.lblDeckName.setObjectName("lblDeckName")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(210, 57, 41, 18))
        self.label_2.setObjectName("label_2")
        self.lblCardsQnt = QtWidgets.QLabel(self.centralwidget)
        self.lblCardsQnt.setGeometry(QtCore.QRect(260, 57, 101, 18))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lblCardsQnt.sizePolicy().hasHeightForWidth())
        self.lblCardsQnt.setSizePolicy(sizePolicy)
        self.lblCardsQnt.setObjectName("lblCardsQnt")
        self.pBarHitsPercentage = QtWidgets.QProgressBar(self.centralwidget)
        self.pBarHitsPercentage.setGeometry(QtCore.QRect(30, 20, 251, 20))
        self.pBarHitsPercentage.setProperty("value", 24)
        self.pBarHitsPercentage.setObjectName("pBarHitsPercentage")
        self.plainTextEdit.raise_()
        self.btnUnsatisfactory.raise_()
        self.btnNormal.raise_()
        self.btnVeryGood.raise_()
        self.btnRevealAnswer.raise_()
        self.label.raise_()
        self.lblDeckName.raise_()
        self.label_2.raise_()
        self.lblCardsQnt.raise_()
        self.pBarHitsPercentage.raise_()
        StudyCardsWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(StudyCardsWindow)
        self.statusbar.setObjectName("statusbar")
        StudyCardsWindow.setStatusBar(self.statusbar)

        self.retranslateUi(StudyCardsWindow)
        QtCore.QMetaObject.connectSlotsByName(StudyCardsWindow)

    def retranslateUi(self, StudyCardsWindow):
        _translate = QtCore.QCoreApplication.translate
        StudyCardsWindow.setWindowTitle(_translate("StudyCardsWindow", "StudyCardsWindow"))
        self.btnRevealAnswer.setText(_translate("StudyCardsWindow", "Reveal Answer"))
        self.btnUnsatisfactory.setText(_translate("StudyCardsWindow", ":("))
        self.btnNormal.setText(_translate("StudyCardsWindow", ":|"))
        self.btnVeryGood.setText(_translate("StudyCardsWindow", ":D"))
        self.label.setText(_translate("StudyCardsWindow", "Deck."))
        self.lblDeckName.setText(_translate("StudyCardsWindow", "lblDeckName"))
        self.label_2.setText(_translate("StudyCardsWindow", "Card."))
        self.lblCardsQnt.setText(_translate("StudyCardsWindow", "0/0"))