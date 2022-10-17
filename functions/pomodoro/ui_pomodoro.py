from PySide6 import QtCore, QtGui, QtWidgets
from PySide6.QtWidgets import QSizePolicy

from PySide6.QtCore import Qt, QTime, QTimer, QSettings, QDir
from PySide6.QtWidgets import (
    QAbstractItemView,
    QApplication,
    QComboBox,
    QFormLayout,
    QGroupBox,
    QHBoxLayout,
    QHeaderView,
    QLabel,
    QLCDNumber,
    QMainWindow,
    QMenu,
    QPushButton,
    QSizePolicy,
    QSpinBox,
    QSystemTrayIcon,
    QTableWidget,
    QTableWidgetItem,
    QTabWidget,
    QTextEdit,
    QToolButton,
    QVBoxLayout,
    QWidget,
)
from .const import *

class Ui_PomodoroPage(object):
    def setupUi(self, Widget):
        Widget.setObjectName("Widget")
        Widget.resize(800, 600)
        self.tblTasks = QtWidgets.QTableWidget(Widget)
        self.tblTasks.setGeometry(QtCore.QRect(380, 70, 256, 192))
        self.tblTasks.setObjectName("tblTasks")
        self.tblTasks.setColumnCount(0)
        self.tblTasks.setRowCount(0)
        self.frame = QtWidgets.QFrame(Widget)
        self.frame.setGeometry(QtCore.QRect(10, 70, 351, 481))
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.btnPomodoro = QtWidgets.QPushButton(self.frame)
        self.btnPomodoro.setGeometry(QtCore.QRect(10, 70, 91, 26))
        self.btnPomodoro.setObjectName("btnPomodoro")
        self.lblTask = QtWidgets.QLabel(self.frame)
        self.lblTask.setGeometry(QtCore.QRect(40, 380, 361, 20))
        self.lblTask.setObjectName("lblTask")
        self.timeDisplay = QtWidgets.QLCDNumber(8, self.frame)
        self.timeDisplay.setGeometry(QtCore.QRect(10, 110, 331, 181))
        self.timeDisplay.setObjectName("timeDisplay")
        self.timeDisplay.setFixedHeight(100)
        self.timeDisplay.display("00:00:00")
        self.btnShortRest = QtWidgets.QPushButton(self.frame)
        self.btnShortRest.setGeometry(QtCore.QRect(110, 70, 111, 26))
        self.btnShortRest.setObjectName("btnShortRest")
        self.btnLongRest = QtWidgets.QPushButton(self.frame)
        self.btnLongRest.setGeometry(QtCore.QRect(230, 70, 111, 26))
        self.btnLongRest.setObjectName("btnLongRest")
        self.btnAction = QtWidgets.QPushButton(self.frame)
        self.btnAction.setGeometry(QtCore.QRect(100, 310, 91, 41))
        self.btnAction.setObjectName("btnAction")
        self.btnReset = QtWidgets.QPushButton(self.frame)
        self.btnReset.setGeometry(QtCore.QRect(210, 310, 41, 41))
        self.btnReset.setObjectName("btnReset")
        self.progressBar = QtWidgets.QProgressBar(self.frame)
        self.progressBar.setGeometry(QtCore.QRect(10, 30, 331, 23))
        self.progressBar.setProperty("value", 24)
        self.progressBar.setObjectName("progressBar")
        self.btnSettings = QtWidgets.QPushButton(Widget)
        self.btnSettings.setGeometry(QtCore.QRect(270, 30, 88, 26))
        self.btnSettings.setObjectName("btnSettings")

        self.retranslateUi(Widget)
        QtCore.QMetaObject.connectSlotsByName(Widget)

    def retranslateUi(self, Widget):
        _translate = QtCore.QCoreApplication.translate
        Widget.setWindowTitle(_translate("Widget", "Widget"))
        self.btnPomodoro.setText(_translate("Widget", "Pomodoro"))
        self.lblTask.setText(_translate("Widget", "Tarefa Vigente"))
        self.btnShortRest.setText(_translate("Widget", "Descanso Curto"))
        self.btnLongRest.setText(_translate("Widget", "Descanso Longo"))
        self.btnAction.setText(_translate("Widget", "Start"))
        self.btnReset.setText(_translate("Widget", "Reset"))
        self.btnSettings.setText(_translate("Widget", "Setting"))

class Ui_SettingsWindow(object):
    def setupUi(self, Widget):
        Widget.setObjectName("Widget")
        Widget.resize(200, 200)
        self.size_policy = sizePolicy = QSizePolicy(
            QSizePolicy.Expanding, QSizePolicy.Expanding
        )
        settings = QSettings()

        self.timerContainer = QWidget(Widget)
        self.timerContainerLayout = QVBoxLayout(self.timerContainer)
        self.timerContainer.setLayout(self.timerContainerLayout)

        """ Create work groupbox"""
        self.workGroupBox = QGroupBox("Work")
        self.workGroupBoxLayout = QHBoxLayout(self.workGroupBox)
        self.workGroupBox.setLayout(self.workGroupBoxLayout)
        self.workHoursSpinBox = QSpinBox(
            minimum=0,
            maximum=24,
            value=int(settings.value(workHoursKey, 0)),
            suffix="h",
            sizePolicy=self.size_policy,
        )
        self.workMinutesSpinBox = QSpinBox(
            minimum=0,
            maximum=60,
            value=int(settings.value(workMinutesKey, 25)),
            suffix="m",
            sizePolicy=self.size_policy,
        )
        self.workSecondsSpinBox = QSpinBox(
            minimum=0,
            maximum=60,
            value=int(settings.value(workSecondsKey, 0)),
            suffix="s",
            sizePolicy=self.size_policy,
        )
        """ Create rest groupbox"""
        self.restGroupBox = QGroupBox("Rest")
        self.restGroupBoxLayout = QHBoxLayout(self.restGroupBox)
        self.restGroupBox.setLayout(self.restGroupBoxLayout)
        self.restHoursSpinBox = QSpinBox(
            minimum=0,
            maximum=24,
            value=int(settings.value(restHoursKey, 0)),
            suffix="h",
            sizePolicy=self.size_policy,
        )
        self.restMinutesSpinBox = QSpinBox(
            minimum=0,
            maximum=60,
            value=int(settings.value(restMinutesKey, 5)),
            suffix="m",
            sizePolicy=self.size_policy,
        )
        self.restSecondsSpinBox = QSpinBox(
            minimum=0,
            maximum=60,
            value=int(settings.value(restSecondsKey, 0)),
            suffix="s",
            sizePolicy=self.size_policy,
        )
        self.restGroupBoxLayout.addWidget(self.restHoursSpinBox)
        self.restGroupBoxLayout.addWidget(self.restMinutesSpinBox)
        self.restGroupBoxLayout.addWidget(self.restSecondsSpinBox)

        """ Create other groupbox"""
        self.otherGroupBox = QGroupBox("Other")
        self.otherGroupBoxLayout = QHBoxLayout(self.otherGroupBox)
        self.otherGroupBox.setLayout(self.otherGroupBoxLayout)
        self.repetitionsLabel = QLabel("Repetitions")
        self.repetitionsSpinBox = QSpinBox(
            minimum=0,
            maximum=10000,
            value=0,
            sizePolicy=self.size_policy,
            specialValueText="∞",
        )
        self.modeLabel = QLabel("Mode")
        self.modeComboBox = QComboBox(sizePolicy=self.size_policy)
        self.modeComboBox.addItems(["work", "rest"])
        self.otherGroupBoxLayout.addWidget(self.repetitionsLabel)
        self.otherGroupBoxLayout.addWidget(self.repetitionsSpinBox)
        self.otherGroupBoxLayout.addWidget(self.modeLabel)
        self.otherGroupBoxLayout.addWidget(self.modeComboBox)

        """ Add widgets to container """
        self.workGroupBoxLayout.addWidget(self.workHoursSpinBox)
        self.workGroupBoxLayout.addWidget(self.workMinutesSpinBox)
        self.workGroupBoxLayout.addWidget(self.workSecondsSpinBox)
        self.timerContainerLayout.addWidget(self.workGroupBox)
        self.timerContainerLayout.addWidget(self.restGroupBox)
        self.timerContainerLayout.addWidget(self.otherGroupBox)

        Widget.setCentralWidget(self.timerContainer)

        self.retranslateUi(Widget)
        QtCore.QMetaObject.connectSlotsByName(Widget)

    def retranslateUi(self, Widget):
        _translate = QtCore.QCoreApplication.translate
        Widget.setWindowTitle(_translate("Widget", "Widget"))

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Widget = QtWidgets.QWidget()
    ui = Ui_PomodoroPage()
    ui.setupUi(Widget)
    Widget.show()
    sys.exit(app.exec())
