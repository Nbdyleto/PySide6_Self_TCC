# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'new_pomodoro_page.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PySide6 import QtCore, QtGui, QtWidgets


class Ui_Widget(object):
    def setupUi(self, Widget):
        Widget.setObjectName("Widget")
        Widget.resize(800, 600)
        self.horizontalLayout = QtWidgets.QHBoxLayout(Widget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.tabWidget = QtWidgets.QTabWidget(Widget)
        self.tabWidget.setMinimumSize(QtCore.QSize(600, 0))
        self.tabWidget.setStyleSheet("font: 18px;\n"
"")
        self.tabWidget.setObjectName("tabWidget")
        self.tabWidgetPage1 = QtWidgets.QWidget()
        self.tabWidgetPage1.setObjectName("tabWidgetPage1")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.tabWidgetPage1)
        self.verticalLayout.setObjectName("verticalLayout")
        self.frame_13 = QtWidgets.QFrame(self.tabWidgetPage1)
        self.frame_13.setMinimumSize(QtCore.QSize(600, 0))
        self.frame_13.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_13.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_13.setObjectName("frame_13")
        self.verticalLayout_8 = QtWidgets.QVBoxLayout(self.frame_13)
        self.verticalLayout_8.setObjectName("verticalLayout_8")
        self.frame = QtWidgets.QFrame(self.frame_13)
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.frame)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.frame_8 = QtWidgets.QFrame(self.frame)
        self.frame_8.setMaximumSize(QtCore.QSize(16777215, 50))
        self.frame_8.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_8.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_8.setObjectName("frame_8")
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout(self.frame_8)
        self.horizontalLayout_7.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_7.setSpacing(2)
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.progressBar = QtWidgets.QProgressBar(self.frame_8)
        self.progressBar.setCursor(QtGui.QCursor(QtCore.Qt.CrossCursor))
        self.progressBar.setMaximum(100)
        self.progressBar.setProperty("value", 0)
        self.progressBar.setTextVisible(False)
        self.progressBar.setObjectName("progressBar")
        self.horizontalLayout_7.addWidget(self.progressBar)
        self.verticalLayout_2.addWidget(self.frame_8)
        self.frame_3 = QtWidgets.QFrame(self.frame)
        self.frame_3.setMaximumSize(QtCore.QSize(16777215, 50))
        self.frame_3.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_3.setObjectName("frame_3")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.frame_3)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.btnPomodoro = QtWidgets.QPushButton(self.frame_3)
        self.btnPomodoro.setMinimumSize(QtCore.QSize(90, 40))
        self.btnPomodoro.setMaximumSize(QtCore.QSize(200, 16777215))
        self.btnPomodoro.setStyleSheet("background-repeat: no-repeat; \n"
"border-radius: 20px;\n"
"text-align: center;\n"
"font: bold;")
        self.btnPomodoro.setObjectName("btnPomodoro")
        self.horizontalLayout_2.addWidget(self.btnPomodoro)
        self.btnShortRest = QtWidgets.QPushButton(self.frame_3)
        self.btnShortRest.setMinimumSize(QtCore.QSize(120, 40))
        self.btnShortRest.setMaximumSize(QtCore.QSize(200, 16777215))
        self.btnShortRest.setStyleSheet("background-repeat: no-repeat; \n"
"border-radius: 20px;\n"
"text-align: center;\n"
"font: bold;")
        self.btnShortRest.setObjectName("btnShortRest")
        self.horizontalLayout_2.addWidget(self.btnShortRest)
        self.btnLongRest = QtWidgets.QPushButton(self.frame_3)
        self.btnLongRest.setMinimumSize(QtCore.QSize(120, 40))
        self.btnLongRest.setMaximumSize(QtCore.QSize(200, 16777215))
        self.btnLongRest.setStyleSheet("background-repeat: no-repeat; \n"
"border-radius: 20px;\n"
"text-align: center;\n"
"font: bold;")
        self.btnLongRest.setObjectName("btnLongRest")
        self.horizontalLayout_2.addWidget(self.btnLongRest)
        self.verticalLayout_2.addWidget(self.frame_3)
        self.lcdPomodoroTimer = QtWidgets.QLCDNumber(self.frame)
        font = QtGui.QFont()
        font.setPointSize(-1)
        font.setBold(False)
        font.setItalic(False)
        self.lcdPomodoroTimer.setFont(font)
        self.lcdPomodoroTimer.setDigitCount(5)
        self.lcdPomodoroTimer.setProperty("intValue", 0)
        self.lcdPomodoroTimer.setObjectName("lcdPomodoroTimer")
        self.verticalLayout_2.addWidget(self.lcdPomodoroTimer)
        self.frame_4 = QtWidgets.QFrame(self.frame)
        self.frame_4.setMinimumSize(QtCore.QSize(0, 0))
        self.frame_4.setMaximumSize(QtCore.QSize(16777215, 50))
        self.frame_4.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_4.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_4.setObjectName("frame_4")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.frame_4)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.btnStartTimer = QtWidgets.QPushButton(self.frame_4)
        self.btnStartTimer.setMinimumSize(QtCore.QSize(100, 40))
        self.btnStartTimer.setMaximumSize(QtCore.QSize(150, 16777215))
        self.btnStartTimer.setStyleSheet("background-repeat: no-repeat; \n"
"border-radius: 20px;\n"
"text-align: center;")
        self.btnStartTimer.setObjectName("btnStartTimer")
        self.horizontalLayout_3.addWidget(self.btnStartTimer)
        self.btnPauseTimer = QtWidgets.QPushButton(self.frame_4)
        self.btnPauseTimer.setMinimumSize(QtCore.QSize(100, 40))
        self.btnPauseTimer.setMaximumSize(QtCore.QSize(150, 16777215))
        self.btnPauseTimer.setStyleSheet("background-repeat: no-repeat; \n"
"border-radius: 20px;\n"
"text-align: center;")
        self.btnPauseTimer.setObjectName("btnPauseTimer")
        self.horizontalLayout_3.addWidget(self.btnPauseTimer)
        self.btnResetTimer = QtWidgets.QPushButton(self.frame_4)
        self.btnResetTimer.setMinimumSize(QtCore.QSize(100, 40))
        self.btnResetTimer.setMaximumSize(QtCore.QSize(150, 16777215))
        self.btnResetTimer.setStyleSheet("background-repeat: no-repeat; \n"
"border-radius: 20px;\n"
"text-align: center;")
        self.btnResetTimer.setObjectName("btnResetTimer")
        self.horizontalLayout_3.addWidget(self.btnResetTimer)
        self.verticalLayout_2.addWidget(self.frame_4)
        self.frame_5 = QtWidgets.QFrame(self.frame)
        self.frame_5.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_5.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_5.setObjectName("frame_5")
        self.verticalLayout_9 = QtWidgets.QVBoxLayout(self.frame_5)
        self.verticalLayout_9.setObjectName("verticalLayout_9")
        self.lblActualTask = QtWidgets.QLabel(self.frame_5)
        self.lblActualTask.setStyleSheet("font: bold 20px;")
        self.lblActualTask.setObjectName("lblActualTask")
        self.verticalLayout_9.addWidget(self.lblActualTask, 0, QtCore.Qt.AlignHCenter)
        self.lblStudyCount = QtWidgets.QLabel(self.frame_5)
        self.lblStudyCount.setObjectName("lblStudyCount")
        self.verticalLayout_9.addWidget(self.lblStudyCount, 0, QtCore.Qt.AlignHCenter)
        self.verticalLayout_2.addWidget(self.frame_5)
        self.verticalLayout_8.addWidget(self.frame)
        self.verticalLayout.addWidget(self.frame_13, 0, QtCore.Qt.AlignHCenter)
        self.tabWidget.addTab(self.tabWidgetPage1, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.verticalLayout_6 = QtWidgets.QVBoxLayout(self.tab_2)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.frame_14 = QtWidgets.QFrame(self.tab_2)
        self.frame_14.setMinimumSize(QtCore.QSize(600, 0))
        self.frame_14.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_14.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_14.setObjectName("frame_14")
        self.verticalLayout_10 = QtWidgets.QVBoxLayout(self.frame_14)
        self.verticalLayout_10.setObjectName("verticalLayout_10")
        self.frame_7 = QtWidgets.QFrame(self.frame_14)
        self.frame_7.setMinimumSize(QtCore.QSize(0, 0))
        self.frame_7.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_7.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_7.setObjectName("frame_7")
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout(self.frame_7)
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.tblTasks = QtWidgets.QTableWidget(self.frame_7)
        self.tblTasks.setMinimumSize(QtCore.QSize(0, 0))
        self.tblTasks.setMaximumSize(QtCore.QSize(500, 16777215))
        self.tblTasks.viewport().setProperty("cursor", QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.tblTasks.setFocusPolicy(QtCore.Qt.NoFocus)
        self.tblTasks.setStyleSheet("font: 15px;\n"
"")
        self.tblTasks.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.tblTasks.setSelectionMode(QtWidgets.QAbstractItemView.NoSelection)
        self.tblTasks.setShowGrid(False)
        self.tblTasks.setObjectName("tblTasks")
        self.tblTasks.setColumnCount(2)
        self.tblTasks.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.tblTasks.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tblTasks.setHorizontalHeaderItem(1, item)
        self.tblTasks.verticalHeader().setVisible(False)
        self.horizontalLayout_6.addWidget(self.tblTasks)
        self.verticalLayout_10.addWidget(self.frame_7)
        self.verticalLayout_6.addWidget(self.frame_14, 0, QtCore.Qt.AlignHCenter)
        self.frame_6 = QtWidgets.QFrame(self.tab_2)
        self.frame_6.setMaximumSize(QtCore.QSize(16777215, 150))
        self.frame_6.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_6.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_6.setObjectName("frame_6")
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout(self.frame_6)
        self.horizontalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.verticalLayout_6.addWidget(self.frame_6, 0, QtCore.Qt.AlignHCenter)
        self.tabWidget.addTab(self.tab_2, "")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.tab)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.frame_15 = QtWidgets.QFrame(self.tab)
        self.frame_15.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_15.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_15.setObjectName("frame_15")
        self.horizontalLayout_8 = QtWidgets.QHBoxLayout(self.frame_15)
        self.horizontalLayout_8.setObjectName("horizontalLayout_8")
        self.frame_10 = QtWidgets.QFrame(self.frame_15)
        self.frame_10.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_10.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_10.setObjectName("frame_10")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.frame_10)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.frame_11 = QtWidgets.QFrame(self.frame_10)
        self.frame_11.setMaximumSize(QtCore.QSize(16777215, 120))
        self.frame_11.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_11.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_11.setObjectName("frame_11")
        self.horizontalLayout_13 = QtWidgets.QHBoxLayout(self.frame_11)
        self.horizontalLayout_13.setObjectName("horizontalLayout_13")
        self.workGroupBox = QtWidgets.QGroupBox(self.frame_11)
        self.workGroupBox.setObjectName("workGroupBox")
        self.horizontalLayout_11 = QtWidgets.QHBoxLayout(self.workGroupBox)
        self.horizontalLayout_11.setObjectName("horizontalLayout_11")
        self.workMinutesSpinBox = QtWidgets.QSpinBox(self.workGroupBox)
        self.workMinutesSpinBox.setMaximumSize(QtCore.QSize(65, 16777215))
        self.workMinutesSpinBox.setMinimum(1)
        self.workMinutesSpinBox.setMaximum(59)
        self.workMinutesSpinBox.setObjectName("workMinutesSpinBox")
        self.horizontalLayout_11.addWidget(self.workMinutesSpinBox)
        self.horizontalLayout_13.addWidget(self.workGroupBox)
        self.shortRestGroupBox = QtWidgets.QGroupBox(self.frame_11)
        self.shortRestGroupBox.setObjectName("shortRestGroupBox")
        self.horizontalLayout_10 = QtWidgets.QHBoxLayout(self.shortRestGroupBox)
        self.horizontalLayout_10.setObjectName("horizontalLayout_10")
        self.shortMinutesSpinBox = QtWidgets.QSpinBox(self.shortRestGroupBox)
        self.shortMinutesSpinBox.setMaximumSize(QtCore.QSize(65, 16777215))
        self.shortMinutesSpinBox.setMinimum(1)
        self.shortMinutesSpinBox.setMaximum(59)
        self.shortMinutesSpinBox.setObjectName("shortMinutesSpinBox")
        self.horizontalLayout_10.addWidget(self.shortMinutesSpinBox)
        self.horizontalLayout_13.addWidget(self.shortRestGroupBox)
        self.groupBox_3 = QtWidgets.QGroupBox(self.frame_11)
        self.groupBox_3.setObjectName("groupBox_3")
        self.horizontalLayout_9 = QtWidgets.QHBoxLayout(self.groupBox_3)
        self.horizontalLayout_9.setObjectName("horizontalLayout_9")
        self.longMinutesSpinBox = QtWidgets.QSpinBox(self.groupBox_3)
        self.longMinutesSpinBox.setMaximumSize(QtCore.QSize(65, 16777215))
        self.longMinutesSpinBox.setMinimum(1)
        self.longMinutesSpinBox.setMaximum(360)
        self.longMinutesSpinBox.setObjectName("longMinutesSpinBox")
        self.horizontalLayout_9.addWidget(self.longMinutesSpinBox)
        self.horizontalLayout_13.addWidget(self.groupBox_3)
        self.verticalLayout_3.addWidget(self.frame_11)
        self.frame_12 = QtWidgets.QFrame(self.frame_10)
        self.frame_12.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_12.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_12.setObjectName("frame_12")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.frame_12)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.groupBox = QtWidgets.QGroupBox(self.frame_12)
        self.groupBox.setCheckable(False)
        self.groupBox.setObjectName("groupBox")
        self.horizontalLayout_12 = QtWidgets.QHBoxLayout(self.groupBox)
        self.horizontalLayout_12.setObjectName("horizontalLayout_12")
        self.rdbtnYesPauseAuto = QtWidgets.QRadioButton(self.groupBox)
        self.rdbtnYesPauseAuto.setChecked(False)
        self.rdbtnYesPauseAuto.setObjectName("rdbtnYesPauseAuto")
        self.horizontalLayout_12.addWidget(self.rdbtnYesPauseAuto)
        self.rdbtnNoPauseAuto = QtWidgets.QRadioButton(self.groupBox)
        self.rdbtnNoPauseAuto.setChecked(True)
        self.rdbtnNoPauseAuto.setObjectName("rdbtnNoPauseAuto")
        self.horizontalLayout_12.addWidget(self.rdbtnNoPauseAuto)
        self.verticalLayout_4.addWidget(self.groupBox)
        self.groupBox_2 = QtWidgets.QGroupBox(self.frame_12)
        self.groupBox_2.setObjectName("groupBox_2")
        self.horizontalLayout_14 = QtWidgets.QHBoxLayout(self.groupBox_2)
        self.horizontalLayout_14.setObjectName("horizontalLayout_14")
        self.rdbtnYesPomoAuto = QtWidgets.QRadioButton(self.groupBox_2)
        self.rdbtnYesPomoAuto.setChecked(False)
        self.rdbtnYesPomoAuto.setObjectName("rdbtnYesPomoAuto")
        self.horizontalLayout_14.addWidget(self.rdbtnYesPomoAuto)
        self.rdbtnNoPomoAuto = QtWidgets.QRadioButton(self.groupBox_2)
        self.rdbtnNoPomoAuto.setChecked(True)
        self.rdbtnNoPomoAuto.setObjectName("rdbtnNoPomoAuto")
        self.horizontalLayout_14.addWidget(self.rdbtnNoPomoAuto)
        self.verticalLayout_4.addWidget(self.groupBox_2)
        self.groupBox_4 = QtWidgets.QGroupBox(self.frame_12)
        self.groupBox_4.setObjectName("groupBox_4")
        self.horizontalLayout_15 = QtWidgets.QHBoxLayout(self.groupBox_4)
        self.horizontalLayout_15.setObjectName("horizontalLayout_15")
        self.rdbtnActivedAlarm = QtWidgets.QRadioButton(self.groupBox_4)
        self.rdbtnActivedAlarm.setChecked(True)
        self.rdbtnActivedAlarm.setObjectName("rdbtnActivedAlarm")
        self.horizontalLayout_15.addWidget(self.rdbtnActivedAlarm)
        self.rdbtnDeactivedAlarm = QtWidgets.QRadioButton(self.groupBox_4)
        self.rdbtnDeactivedAlarm.setObjectName("rdbtnDeactivedAlarm")
        self.horizontalLayout_15.addWidget(self.rdbtnDeactivedAlarm)
        self.verticalLayout_4.addWidget(self.groupBox_4)
        self.btnSaveSettings = QtWidgets.QPushButton(self.frame_12)
        self.btnSaveSettings.setMinimumSize(QtCore.QSize(220, 50))
        self.btnSaveSettings.setStyleSheet("background-position: center;  \n"
"background-repeat: no-repeat; \n"
"border-radius: 25px;\n"
"font: 18px;")
        self.btnSaveSettings.setObjectName("btnSaveSettings")
        self.verticalLayout_4.addWidget(self.btnSaveSettings, 0, QtCore.Qt.AlignHCenter)
        self.verticalLayout_3.addWidget(self.frame_12)
        self.horizontalLayout_8.addWidget(self.frame_10)
        self.verticalLayout_5.addWidget(self.frame_15, 0, QtCore.Qt.AlignHCenter)
        self.tabWidget.addTab(self.tab, "")
        self.horizontalLayout.addWidget(self.tabWidget)

        self.retranslateUi(Widget)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(Widget)

    def retranslateUi(self, Widget):
        _translate = QtCore.QCoreApplication.translate
        Widget.setWindowTitle(_translate("Widget", "Widget"))
        self.btnPomodoro.setText(_translate("Widget", "Pomodoro"))
        self.btnShortRest.setText(_translate("Widget", "Descanso Curto"))
        self.btnLongRest.setText(_translate("Widget", "Descanso Longo"))
        self.btnStartTimer.setText(_translate("Widget", "Iniciar"))
        self.btnPauseTimer.setText(_translate("Widget", "Pausar"))
        self.btnResetTimer.setText(_translate("Widget", "Resetar"))
        self.lblActualTask.setText(_translate("Widget", "Selecione uma tarefa na aba \"Tarefas\" desta p??gina..."))
        self.lblStudyCount.setText(_translate("Widget", "N??mero de estudos:"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabWidgetPage1), _translate("Widget", "Pomodoro"))
        item = self.tblTasks.horizontalHeaderItem(0)
        item.setText(_translate("Widget", "Nome"))
        item = self.tblTasks.horizontalHeaderItem(1)
        item.setText(_translate("Widget", "T??pico"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("Widget", "Tarefas"))
        self.workGroupBox.setTitle(_translate("Widget", "Trabalho"))
        self.workMinutesSpinBox.setSuffix(_translate("Widget", "m"))
        self.shortRestGroupBox.setTitle(_translate("Widget", "Descanso Curto"))
        self.shortMinutesSpinBox.setSuffix(_translate("Widget", "m"))
        self.groupBox_3.setTitle(_translate("Widget", "Descanso Longo"))
        self.longMinutesSpinBox.setSuffix(_translate("Widget", "m"))
        self.groupBox.setTitle(_translate("Widget", "Pausas Autom??ticas"))
        self.rdbtnYesPauseAuto.setText(_translate("Widget", "Sim"))
        self.rdbtnNoPauseAuto.setText(_translate("Widget", "N??o"))
        self.groupBox_2.setTitle(_translate("Widget", "Pomodoros Autom??ticos"))
        self.rdbtnYesPomoAuto.setText(_translate("Widget", "Sim"))
        self.rdbtnNoPomoAuto.setText(_translate("Widget", "N??o"))
        self.groupBox_4.setTitle(_translate("Widget", "Alarme"))
        self.rdbtnActivedAlarm.setText(_translate("Widget", "Ativado"))
        self.rdbtnDeactivedAlarm.setText(_translate("Widget", "Desativado"))
        self.btnSaveSettings.setText(_translate("Widget", "Salvar Configura????es"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("Widget", "Configura????es"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Widget = QtWidgets.QWidget()
    ui = Ui_Widget()
    ui.setupUi(Widget)
    Widget.show()
    sys.exit(app.exec_())
