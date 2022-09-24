# Form implementation generated from reading ui file 'main_ui.ui'
#
# Created by: PyQt6 UI code generator 6.3.0
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PySide6 import QtCore, QtGui, QtWidgets
from .circular_progress import CircularProgress

class Ui_Pomodoro(object):
    def setupUi(self, Widget):
        Widget.setObjectName("Widget")
        Widget.resize(800, 600)
        Widget.setStyleSheet("background-color: black")
        self.verticalLayout = QtWidgets.QVBoxLayout(Widget)
        self.verticalLayout.setContentsMargins(15, 35, 15, 60)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setContentsMargins(-1, -1, -1, 40)
        self.horizontalLayout.setObjectName("horizontalLayout")

        self.progress = CircularProgress()
        self.progress.setMinimumSize(self.progress.width, self.progress.height)
        self.horizontalLayout.addWidget(self.progress, 0, QtCore.Qt.AlignmentFlag.AlignHCenter)
        """
        self.progress = 
        self.progress.setMinimumSize(QtCore.QSize(200, 200))
        self.progress.setObjectName("progress")
        self.horizontalLayout.addWidget(self.progress)
        """
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.button = QtWidgets.QPushButton(Widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.button.sizePolicy().hasHeightForWidth())
        self.button.setSizePolicy(sizePolicy)
        self.button.setMinimumSize(QtCore.QSize(40, 40))
        self.button.setMaximumSize(QtCore.QSize(40, 40))
        self.button.setBaseSize(QtCore.QSize(0, 0))
        self.button.setStyleSheet("background-color: rgb(255, 37, 51);\n"
"background-image: url(\"./play.png\");\n"
"border: 1px solid rgb(255, 37, 51);\n"
"border-radius: 20px;")
        self.button.setText("")
        self.button.setFlat(True)
        self.button.setObjectName("button")
        self.verticalLayout.addWidget(self.button, 1, QtCore.Qt.AlignmentFlag.AlignHCenter)
        self.menuBar = QtWidgets.QMenuBar(Widget)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 800, 30))
        self.menuBar.setObjectName("menuBar")
        self.menuFile = QtWidgets.QMenu(self.menuBar)
        self.menuFile.setObjectName("menuFile")
        self.retranslateUi(Widget)
        QtCore.QMetaObject.connectSlotsByName(Widget)

    def retranslateUi(self, Widget):
        _translate = QtCore.QCoreApplication.translate
        Widget.setWindowTitle(_translate("Widget", "CherryTomato"))
        self.menuFile.setTitle(_translate("Widget", "File"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Widget = QtWidgets.QWidget()
    ui = Ui_Pomodoro()
    ui.setupUi(Widget)
    Widget.show()
    sys.exit(app.exec())
