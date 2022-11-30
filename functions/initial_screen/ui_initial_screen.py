# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'initial_screen.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PySide6 import QtCore, QtGui, QtWidgets


class Ui_InitialScreen(object):
    def setupUi(self, InitialScreen):
        InitialScreen.setObjectName("InitialScreen")
        InitialScreen.resize(800, 600)
        self.horizontalLayout = QtWidgets.QHBoxLayout(InitialScreen)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.tabWidget = QtWidgets.QTabWidget(InitialScreen)
        self.tabWidget.setStyleSheet("font: 18px;\n"
"")
        self.tabWidget.setObjectName("tabWidget")
        self.tabWelcome = QtWidgets.QWidget()
        self.tabWelcome.setObjectName("tabWelcome")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.tabWelcome)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.widget = QtWidgets.QWidget(self.tabWelcome)
        self.widget.setObjectName("widget")
        self.horizontalLayout_2.addWidget(self.widget)
        self.tabWidget.addTab(self.tabWelcome, "")
        self.tabFlashcards = QtWidgets.QWidget()
        self.tabFlashcards.setObjectName("tabFlashcards")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.tabFlashcards)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.widget_2 = QtWidgets.QWidget(self.tabFlashcards)
        self.widget_2.setObjectName("widget_2")
        self.horizontalLayout_3.addWidget(self.widget_2)
        self.tabWidget.addTab(self.tabFlashcards, "")
        self.tabTasks = QtWidgets.QWidget()
        self.tabTasks.setObjectName("tabTasks")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.tabTasks)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.widget_3 = QtWidgets.QWidget(self.tabTasks)
        self.widget_3.setObjectName("widget_3")
        self.horizontalLayout_4.addWidget(self.widget_3)
        self.tabWidget.addTab(self.tabTasks, "")
        self.tabPomodoro = QtWidgets.QWidget()
        self.tabPomodoro.setObjectName("tabPomodoro")
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout(self.tabPomodoro)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.widget_4 = QtWidgets.QWidget(self.tabPomodoro)
        self.widget_4.setObjectName("widget_4")
        self.horizontalLayout_5.addWidget(self.widget_4)
        self.tabWidget.addTab(self.tabPomodoro, "")
        self.horizontalLayout.addWidget(self.tabWidget)

        self.retranslateUi(InitialScreen)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(InitialScreen)

    def retranslateUi(self, InitialScreen):
        _translate = QtCore.QCoreApplication.translate
        InitialScreen.setWindowTitle(_translate("InitialScreen", "initial_screen"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabWelcome), _translate("InitialScreen", "Boas Vindas!"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabFlashcards), _translate("InitialScreen", "Flashcards"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabTasks), _translate("InitialScreen", "Tarefas"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabPomodoro), _translate("InitialScreen", "Pomodoro"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    InitialScreen = QtWidgets.QWidget()
    ui = Ui_InitialScreen()
    ui.setupUi(InitialScreen)
    InitialScreen.show()
    sys.exit(app.exec_())
