# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'study_flashcards_page.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PySide6 import QtCore, QtGui, QtWidgets


class Ui_StudyPage(object):
    def setupUi(self, Widget):
        Widget.setObjectName("Widget")
        Widget.resize(800, 600)
        self.horizontalLayout = QtWidgets.QHBoxLayout(Widget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.frame = QtWidgets.QFrame(Widget)
        self.frame.setMinimumSize(QtCore.QSize(300, 0))
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.frame)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.frame_7 = QtWidgets.QFrame(self.frame)
        self.frame_7.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_7.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_7.setObjectName("frame_7")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.frame_7)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.btnBackPage = QtWidgets.QPushButton(self.frame_7)
        self.btnBackPage.setObjectName("btnBackPage")
        self.verticalLayout_5.addWidget(self.btnBackPage)
        self.btnClassIcon = QtWidgets.QPushButton(self.frame_7)
        self.btnClassIcon.setObjectName("btnClassIcon")
        self.verticalLayout_5.addWidget(self.btnClassIcon)
        self.btnClassName = QtWidgets.QLabel(self.frame_7)
        self.btnClassName.setObjectName("btnClassName")
        self.verticalLayout_5.addWidget(self.btnClassName)
        self.verticalLayout_4.addWidget(self.frame_7)
        self.frame_8 = QtWidgets.QFrame(self.frame)
        self.frame_8.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_8.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_8.setObjectName("frame_8")
        self.progressBar = QtWidgets.QProgressBar(self.frame_8)
        self.progressBar.setGeometry(QtCore.QRect(10, 10, 261, 23))
        self.progressBar.setProperty("value", 24)
        self.progressBar.setObjectName("progressBar")
        self.verticalLayout_4.addWidget(self.frame_8)
        self.horizontalLayout.addWidget(self.frame)
        self.frame_2 = QtWidgets.QFrame(Widget)
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.frame_2)
        self.verticalLayout.setObjectName("verticalLayout")
        self.frame_3 = QtWidgets.QFrame(self.frame_2)
        self.frame_3.setMinimumSize(QtCore.QSize(0, 100))
        self.frame_3.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_3.setObjectName("frame_3")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.frame_3)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label = QtWidgets.QLabel(self.frame_3)
        self.label.setObjectName("label")
        self.horizontalLayout_2.addWidget(self.label)
        self.lblDeckName = QtWidgets.QLabel(self.frame_3)
        self.lblDeckName.setObjectName("lblDeckName")
        self.horizontalLayout_2.addWidget(self.lblDeckName)
        self.label_2 = QtWidgets.QLabel(self.frame_3)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_2.addWidget(self.label_2)
        self.lblCardsCount = QtWidgets.QLabel(self.frame_3)
        self.lblCardsCount.setObjectName("lblCardsCount")
        self.horizontalLayout_2.addWidget(self.lblCardsCount)
        self.verticalLayout.addWidget(self.frame_3)
        self.frame_4 = QtWidgets.QFrame(self.frame_2)
        self.frame_4.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_4.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_4.setObjectName("frame_4")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.frame_4)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.frame_6 = QtWidgets.QFrame(self.frame_4)
        self.frame_6.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.frame_6.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_6.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_6.setObjectName("frame_6")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.frame_6)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.textEdit = QtWidgets.QTextEdit(self.frame_6)
        self.textEdit.setObjectName("textEdit")
        self.verticalLayout_3.addWidget(self.textEdit)
        self.btnRevealAnswer = QtWidgets.QPushButton(self.frame_6)
        self.btnRevealAnswer.setObjectName("btnRevealAnswer")
        self.verticalLayout_3.addWidget(self.btnRevealAnswer)
        self.verticalLayout_2.addWidget(self.frame_6)
        self.frame_5 = QtWidgets.QFrame(self.frame_4)
        self.frame_5.setMaximumSize(QtCore.QSize(16777215, 50))
        self.frame_5.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_5.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_5.setObjectName("frame_5")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.frame_5)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.btnBadFeedback = QtWidgets.QPushButton(self.frame_5)
        self.btnBadFeedback.setObjectName("btnBadFeedback")
        self.horizontalLayout_3.addWidget(self.btnBadFeedback)
        self.btnOkFeedback = QtWidgets.QPushButton(self.frame_5)
        self.btnOkFeedback.setObjectName("btnOkFeedback")
        self.horizontalLayout_3.addWidget(self.btnOkFeedback)
        self.btnGoodFeedback = QtWidgets.QPushButton(self.frame_5)
        self.btnGoodFeedback.setObjectName("btnGoodFeedback")
        self.horizontalLayout_3.addWidget(self.btnGoodFeedback)
        self.verticalLayout_2.addWidget(self.frame_5)
        self.verticalLayout.addWidget(self.frame_4)
        self.horizontalLayout.addWidget(self.frame_2)

        self.retranslateUi(Widget)
        QtCore.QMetaObject.connectSlotsByName(Widget)

    def retranslateUi(self, Widget):
        _translate = QtCore.QCoreApplication.translate
        Widget.setWindowTitle(_translate("Widget", "Widget"))
        self.btnBackPage.setText(_translate("Widget", "PushButton"))
        self.btnClassIcon.setText(_translate("Widget", "PushButton"))
        self.btnClassName.setText(_translate("Widget", "ClassName"))
        self.label.setText(_translate("Widget", "Deck:"))
        self.lblDeckName.setText(_translate("Widget", "DeckName"))
        self.label_2.setText(_translate("Widget", "Cards:"))
        self.lblCardsCount.setText(_translate("Widget", "0/0"))
        self.btnRevealAnswer.setText(_translate("Widget", "Revelar"))
        self.btnBadFeedback.setText(_translate("Widget", ":("))
        self.btnOkFeedback.setText(_translate("Widget", ":I"))
        self.btnGoodFeedback.setText(_translate("Widget", ":D"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Widget = QtWidgets.QWidget()
    ui = Ui_StudyPage()
    ui.setupUi(Widget)
    Widget.show()
    sys.exit(app.exec_())