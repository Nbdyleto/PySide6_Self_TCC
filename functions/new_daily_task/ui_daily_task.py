# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'new_dailytask_page.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PySide6 import QtCore, QtGui, QtWidgets


class Ui_DailyTaskPage(object):
    def setupUi(self, DailyTaskPage):
        DailyTaskPage.setObjectName("DailyTaskPage")
        DailyTaskPage.resize(800, 600)
        DailyTaskPage.setStyleSheet("QLabel{\n"
"font: 18px;\n"
"}")
        self.verticalLayout = QtWidgets.QVBoxLayout(DailyTaskPage)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(2)
        self.verticalLayout.setObjectName("verticalLayout")
        self.frame = QtWidgets.QFrame(DailyTaskPage)
        self.frame.setMinimumSize(QtCore.QSize(0, 100))
        self.frame.setMaximumSize(QtCore.QSize(500, 195))
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.frame)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setSpacing(2)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.frame_4 = QtWidgets.QFrame(self.frame)
        self.frame_4.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_4.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_4.setObjectName("frame_4")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.frame_4)
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_3.setSpacing(2)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.label = QtWidgets.QLabel(self.frame_4)
        self.label.setStyleSheet("font: italic 15px;")
        self.label.setObjectName("label")
        self.verticalLayout_3.addWidget(self.label)
        self.frame_3 = QtWidgets.QFrame(self.frame_4)
        self.frame_3.setMaximumSize(QtCore.QSize(16777215, 100))
        self.frame_3.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_3.setObjectName("frame_3")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.frame_3)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setSpacing(2)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.listByTopic = QtWidgets.QListWidget(self.frame_3)
        self.listByTopic.setMaximumSize(QtCore.QSize(16777215, 100))
        self.listByTopic.setStyleSheet("font: 18px;")
        self.listByTopic.setObjectName("listByTopic")
        self.horizontalLayout.addWidget(self.listByTopic)
        self.listByStatus = QtWidgets.QListWidget(self.frame_3)
        self.listByStatus.setMaximumSize(QtCore.QSize(16777215, 100))
        self.listByStatus.setStyleSheet("font: 18px;")
        self.listByStatus.setObjectName("listByStatus")
        self.horizontalLayout.addWidget(self.listByStatus)
        self.verticalLayout_3.addWidget(self.frame_3)
        self.horizontalLayout_2.addWidget(self.frame_4, 0, QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.verticalLayout.addWidget(self.frame)
        self.frame_2 = QtWidgets.QFrame(DailyTaskPage)
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.frame_2)
        self.horizontalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_4.setSpacing(2)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.tblTasks = QtWidgets.QTableWidget(self.frame_2)
        self.tblTasks.setMouseTracking(False)
        self.tblTasks.setFocusPolicy(QtCore.Qt.NoFocus)
        self.tblTasks.setStyleSheet("")
        self.tblTasks.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.tblTasks.setSelectionMode(QtWidgets.QAbstractItemView.NoSelection)
        self.tblTasks.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.tblTasks.setShowGrid(False)
        self.tblTasks.setObjectName("tblTasks")
        self.tblTasks.setColumnCount(7)
        self.tblTasks.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.tblTasks.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tblTasks.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tblTasks.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tblTasks.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.tblTasks.setHorizontalHeaderItem(4, item)
        item = QtWidgets.QTableWidgetItem()
        self.tblTasks.setHorizontalHeaderItem(5, item)
        item = QtWidgets.QTableWidgetItem()
        self.tblTasks.setHorizontalHeaderItem(6, item)
        self.tblTasks.horizontalHeader().setHighlightSections(False)
        self.tblTasks.verticalHeader().setVisible(False)
        self.tblTasks.verticalHeader().setHighlightSections(False)
        self.horizontalLayout_4.addWidget(self.tblTasks)
        self.specialFrame = QtWidgets.QFrame(self.frame_2)
        self.specialFrame.setMaximumSize(QtCore.QSize(270, 250))
        self.specialFrame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.specialFrame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.specialFrame.setObjectName("specialFrame")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.specialFrame)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setSpacing(2)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.lblSetInfo = QtWidgets.QLabel(self.specialFrame)
        self.lblSetInfo.setObjectName("lblSetInfo")
        self.verticalLayout_2.addWidget(self.lblSetInfo)
        self.frame_5 = QtWidgets.QFrame(self.specialFrame)
        self.frame_5.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_5.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_5.setObjectName("frame_5")
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout(self.frame_5)
        self.horizontalLayout_6.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_6.setSpacing(2)
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.qCalendar = QtWidgets.QCalendarWidget(self.frame_5)
        self.qCalendar.setObjectName("qCalendar")
        self.horizontalLayout_6.addWidget(self.qCalendar)
        self.tblLists = QtWidgets.QTableWidget(self.frame_5)
        self.tblLists.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.tblLists.setAutoScroll(False)
        self.tblLists.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.tblLists.setTabKeyNavigation(False)
        self.tblLists.setSelectionMode(QtWidgets.QAbstractItemView.NoSelection)
        self.tblLists.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.tblLists.setShowGrid(False)
        self.tblLists.setObjectName("tblLists")
        self.tblLists.setColumnCount(0)
        self.tblLists.setRowCount(0)
        self.tblLists.horizontalHeader().setVisible(False)
        self.tblLists.horizontalHeader().setHighlightSections(False)
        self.tblLists.verticalHeader().setVisible(False)
        self.tblLists.verticalHeader().setHighlightSections(False)
        self.horizontalLayout_6.addWidget(self.tblLists)
        self.verticalLayout_2.addWidget(self.frame_5)
        self.horizontalLayout_4.addWidget(self.specialFrame, 0, QtCore.Qt.AlignTop)
        self.verticalLayout.addWidget(self.frame_2)

        self.retranslateUi(DailyTaskPage)
        QtCore.QMetaObject.connectSlotsByName(DailyTaskPage)

    def retranslateUi(self, DailyTaskPage):
        _translate = QtCore.QCoreApplication.translate
        DailyTaskPage.setWindowTitle(_translate("DailyTaskPage", "Widget"))
        self.label.setText(_translate("DailyTaskPage", "Filtrar..."))
        item = self.tblTasks.horizontalHeaderItem(0)
        item.setText(_translate("DailyTaskPage", "Nome"))
        item = self.tblTasks.horizontalHeaderItem(1)
        item.setText(_translate("DailyTaskPage", "Status"))
        item = self.tblTasks.horizontalHeaderItem(2)
        item.setText(_translate("DailyTaskPage", "Data Inicial"))
        item = self.tblTasks.horizontalHeaderItem(3)
        item.setText(_translate("DailyTaskPage", "Data Final"))
        item = self.tblTasks.horizontalHeaderItem(4)
        item.setText(_translate("DailyTaskPage", "Tópico"))
        self.lblSetInfo.setText(_translate("DailyTaskPage", "TextLabel"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    DailyTaskPage = QtWidgets.QWidget()
    ui = Ui_DailyTaskPage()
    ui.setupUi(DailyTaskPage)
    DailyTaskPage.show()
    sys.exit(app.exec_())
