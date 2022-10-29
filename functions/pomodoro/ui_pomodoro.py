from tkinter import Frame
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
    QWidget
)
from .const import *

class Ui_PomodoroPage(object):
    def setupUi(self, Widget):
        Widget.setObjectName("Widget")
        Widget.resize(800, 600)
        Widget.setStyleSheet("""
            QPushButton {	
                background-color: rgb(34, 41, 34);
                border-radius: 15px
            }
            QPushButton:hover {
                background-color: rgb(42, 48, 41);
            }
            QPushButton:pressed {	
                background-color: rgb(94, 171, 79);
                color: black;
            }
        """
        )
        self.tblTasks = QtWidgets.QTableWidget(Widget)
        self.tblTasks.setGeometry(QtCore.QRect(500, 110, 385, 250))
        self.tblTasks.setObjectName("tblTasks")
        self.tblTasks.setColumnCount(2)
        self.tblTasks.setRowCount(1)
        self.tblTasks.verticalHeader().setVisible(False)
        self.tblTasks.horizontalHeader().setVisible(False)
        self.tblTasks.setShowGrid(False)
        self.tblTasks.setColumnWidth(0, 250)
        self.tblTasks.setColumnWidth(1, 100)

        ## meu
        self.tblTasks.setStyleSheet("""
            QTableWidget {
                background-color: rgb(40, 44, 52);
                border-radius: 0px;
            }
            QTableWidget::item {
                color: #f8f8f2;                    
                background-color: rgb(44, 49, 58);;
                margin-top: 2px;          
                border-radius: 0px;
                padding-left: 2px;
            }
            QTableWidget::item:selected {
                background-color: #6272a4;
                selection-color : #f8f8f2;  
            }
            QTableWidget::item:hover {
                background-color: #6272a4;
                color : #f8f8f2;
            }
        """)

        ## juco

        self.tblTasks.setStyleSheet("""
            QTableWidget {	
                background-color: transparent;
                border-radius: 0px;
            }
            QTableWidget::item{
                background-color: rgb(51, 61, 50);
                border-color: rgb(33, 51, 34);
                margin-top: 2px;          
                border-radius: 0px;
                padding-left: 2px;
            }
            QTableWidget::item:selected{
                background-color: rgb(162, 219, 85);
                color: black
            }
            QTableWidget::item:hover {
                background-color: rgb(162, 219, 85);
                color : black;
            }
            QHeaderView::section{
                background-color: rgb(36, 44, 35); 
                max-width: 30px;
                border: 1px solid rgb(51, 61, 50);
                border-style: none;
                border-bottom: 1px solid rgb(45, 48, 43);
                border-right: 1px solid rgb(45, 48, 43);
            }
            QHeaderView::section:vertical
            {
                border: 1px solid rgb(45, 48, 43);
            }
        """)

        self.tblTasks.horizontalHeader().setStretchLastSection(True)
        self.tblTasks.setWordWrap(True)
        self.tblTasks.setTextElideMode(Qt.ElideNone)
        self.tblTasks.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tblTasks.setSelectionMode(QAbstractItemView.SingleSelection)

        self.frame = QtWidgets.QFrame(Widget)
        self.frame.setGeometry(QtCore.QRect(50, 70, 351, 481))
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.lblTask = QtWidgets.QLabel(self.frame)
        self.lblTask.setGeometry(QtCore.QRect(40, 320, 361, 20))
        self.lblTask.setObjectName("lblTask")
        self.timeDisplay = QtWidgets.QLCDNumber(8, self.frame)
        self.timeDisplay.setGeometry(QtCore.QRect(10, 110, 331, 181))
        self.timeDisplay.setObjectName("timeDisplay")
        self.timeDisplay.setFixedHeight(100)
        self.timeDisplay.display("00:00:00")
        self.btnPomodoro = QtWidgets.QPushButton(self.frame)
        self.btnPomodoro.setGeometry(QtCore.QRect(10, 70, 90, 35))
        self.btnPomodoro.setObjectName("btnPomodoro")
        self.btnShortRest = QtWidgets.QPushButton(self.frame)
        self.btnShortRest.setGeometry(QtCore.QRect(105, 70, 120, 35))
        self.btnShortRest.setObjectName("btnShortRest")
        self.btnLongRest = QtWidgets.QPushButton(self.frame)
        self.btnLongRest.setGeometry(QtCore.QRect(230, 70, 120, 35))
        self.btnLongRest.setObjectName("btnLongRest")
        self.btnAction = QtWidgets.QPushButton(self.frame)
        self.btnAction.setGeometry(QtCore.QRect(100, 230, 91, 41))
        self.btnAction.setObjectName("btnAction")
        self.btnReset = QtWidgets.QPushButton(self.frame)
        self.btnReset.setGeometry(QtCore.QRect(210, 230, 41, 41))
        self.btnReset.setObjectName("btnReset")
        self.progressBar = QtWidgets.QProgressBar(self.frame)
        self.progressBar.setGeometry(QtCore.QRect(10, 30, 331, 23))
        self.progressBar.setProperty("value", 24)
        self.progressBar.setObjectName("progressBar")
        
        ## Roxo
        self.progressBar.setStyleSheet("""
        QProgressBar{
            background-color: rgb(44, 49, 58);
            border-color: rgb(44, 49, 58);
            text-align: center;
        }
        QProgressBar::chunk {
            width: 1px;
            background-color: rgb(189, 147, 249);
            border: solid grey;
            border-radius: 15px;
        }    
        """)

        ## Verde
        self.progressBar.setStyleSheet("""
        QProgressBar{
            background-color: rgb(34, 41, 34);
            border-color: rgb(34, 41, 34);
            text-align: center;
        }
        QProgressBar::chunk {
            width: 1px;
            background-color: rgb(162, 219, 85);
            border: solid grey;
            border-radius: 15px;
        }    
        """)

        self.progressBar.setTextVisible(False)
        self.progressBar.setValue(0)
        self.btnSettings = QtWidgets.QPushButton(Widget)
        self.btnSettings.setGeometry(QtCore.QRect(300, 45, 88, 26))
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
        self.btnSettings.setText(_translate("Widget", "Settings"))

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

        self.btnChangeSettings = QPushButton("save")
        self.timerContainerLayout.addWidget(self.btnChangeSettings)

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
