# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.
# to convert in this: python -m PyQt6.uic.pyuic -x addCards.ui -o ui_addCards

from PySide6 import QtCore, QtGui, QtWidgets

class Ui_FlashcardsPage(object):
    def setupUi(self, Widget):
        Widget.setObjectName("Widget")
        Widget.resize(724, 408)
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
        
        self.tblWidgetDecks = QtWidgets.QTableWidget(Widget)
        self.tblWidgetDecks.setGeometry(QtCore.QRect(140, 200, 900, 375))
        self.tblWidgetDecks.setObjectName("tblWidgetDecks")
        self.tblWidgetDecks.setColumnCount(3)
        self.tblWidgetDecks.setRowCount(1)
        self.tblWidgetDecks.setShowGrid(False)
        self.tblWidgetDecks.setFocusPolicy(QtCore.Qt.NoFocus)
        self.tblWidgetDecks.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.tblWidgetDecks.horizontalHeader().setVisible(False)
        self.tblWidgetDecks.verticalHeader().setVisible(False)
        item = QtWidgets.QTableWidgetItem()
        self.tblWidgetDecks.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tblWidgetDecks.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tblWidgetDecks.setHorizontalHeaderItem(2, item)
        self.tblWidgetDecks.setColumnWidth(0,150)
        self.tblWidgetDecks.setColumnWidth(1,500)
        self.tblWidgetDecks.setColumnWidth(2,140)
        self.tblWidgetDecks.setStyleSheet("""
            QTableWidget::item {
                color: #f8f8f2;                    
                background-color: #44475a;
                margin-top: 3px;          
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
        self.tblWidgetDecks.setStyleSheet("""
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
                background-color: rgb(51, 61, 50);
                color: #f8f8f2;
            }
            QHeaderView::section{
                background-color: rgb(36, 44, 35); 
                max-width: 30px;
                border: 1px solid rgb(51, 61, 50);
                border-style: none;
                border-bottom: 1px solid rgb(45, 48, 43);
                border-right: 1px solid rgb(45, 48, 43);
            }
            QHeaderView::section:vertical{
                border: 1px solid rgb(45, 48, 43);
            }
        """)
        self.tblWidgetDecks.setMouseTracking(False)

        self.lblDecks = QtWidgets.QLabel(Widget)
        self.lblDecks.setGeometry(QtCore.QRect(450, 170, 67, 18))
        self.lblDecks.setObjectName("lblDecks")
        self.lblClass = QtWidgets.QLabel(Widget)
        self.lblClass.setGeometry(QtCore.QRect(140, 130, 67, 18))
        self.lblClass.setObjectName("lblClass")

        self.listView = QtWidgets.QListView(Widget)
        self.listView.setGeometry(QtCore.QRect(100, 130, 81, 16))
        self.listView.setObjectName("listView")

        self.pushButton = QtWidgets.QPushButton(Widget)
        self.pushButton.setGeometry(QtCore.QRect(600, 130, 88, 26))
        self.pushButton.setObjectName("pushButton")

        self.btnAddCards = QtWidgets.QPushButton(Widget)
        self.btnAddCards.setGeometry(QtCore.QRect(700, 130, 150, 26))
        self.btnAddCards.setObjectName("btnAddCards")

        self.retranslateUi(Widget)
        QtCore.QMetaObject.connectSlotsByName(Widget)

    def retranslateUi(self, Widget):
        _translate = QtCore.QCoreApplication.translate
        Widget.setWindowTitle(_translate("Widget", u"Flashcards"))
        
        item = self.tblWidgetDecks.horizontalHeaderItem(0)
        item.setText(_translate("Widget", u"hints_percentage"))
        item = self.tblWidgetDecks.horizontalHeaderItem(1)
        item.setText(_translate("Widget", u"deck_name"))
        item = self.tblWidgetDecks.horizontalHeaderItem(2)
        item.setText(_translate("Widget", u"btn_action"))
        
        self.lblDecks.setText(_translate("Widget", u"Decks"))
        self.lblClass.setText(_translate("Widget", u"Classe:"))
        self.pushButton.setText(_translate("Widget", u"Opções"))
        self.btnAddCards.setText(_translate("Widget", u"Adicionar Cards"))

if __name__ == "__main__":
    """Test Individual Execution"""
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Widget = QtWidgets.QWidget()
    ui = Ui_FlashcardsPage()
    ui.setupUi(Widget)
    Widget.show()
    sys.exit(app.exec_())
