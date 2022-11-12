from PySide6 import QtCore, QtGui, QtWidgets, QtCharts

from functions.see_progress.ui_see_progress import Ui_SeeProgressPage

class SeeProgressMainPage(QtWidgets.QWidget):
    def __init__(self):
        super(SeeProgressMainPage, self).__init__()
        self.ui = Ui_SeeProgressPage()
        self.ui.setupUi(self)
        self.setupVariables()
        self.setupWidgets()
        self.setupCharts()

    def setupVariables(self):
        global widgets
        widgets = self.ui

    def setupWidgets(self):
        widgets.tabSeeProgress.setStyleSheet('background-color: rgb(54, 43, 60); color: white; font: 15px;')

    def setupCharts(self):
        # flashcards temp
        series1 = QtCharts.QPieSeries()
        series1.append('Erros', 1)
        series1.append('Acertos', 2)
        slice1 = series1.slices()[1]
        slice1.setExploded()
        slice1.setLabelVisible()
        slice1.setPen(QtGui.QPen(QtCore.Qt.darkGreen, 2))
        slice1.setBrush(QtCore.Qt.green)
        chart1 = QtCharts.QChart()
        chart1.addSeries(series1)
        chart1.setTitle('Simple piechart example')
        chart1.legend().show()
        self._chart_view1 = QtCharts.QChartView(chart1)
        self._chart_view1.setRenderHint(QtGui.QPainter.Antialiasing)

        widgets.verticalLayout_18.addWidget(self._chart_view1)    # verticalLayout_18: Flashcards Frame

        # tasks temp
        series2 = QtCharts.QPieSeries()
        series2.append('Erros', 1)
        series2.append('Acertos', 2)
        slice2 = series2.slices()[1]
        slice2.setExploded()
        slice2.setLabelVisible()
        slice2.setPen(QtGui.QPen(QtCore.Qt.darkGreen, 2))
        slice2.setBrush(QtCore.Qt.green)
        chart2 = QtCharts.QChart()
        chart2.addSeries(series2)
        chart2.setTitle('Simple piechart example')
        chart2.legend().show()
        self._chart_view2 = QtCharts.QChartView(chart2)
        self._chart_view2.setRenderHint(QtGui.QPainter.Antialiasing)

        widgets.verticalLayout_20.addWidget(self._chart_view2)    # verticalLayout_20: Tasks Frame

        #pomodoro temp
        set0 = QtCharts.QBarSet("Parwiz")
        set1 = QtCharts.QBarSet("Bob")
        set2 = QtCharts.QBarSet("Tom")
        set3 = QtCharts.QBarSet("Logan")
        set4 = QtCharts.QBarSet("Karim")
        set0 << 1 << 2 << 3 << 4 << 5 << 6
        set1 << 5 << 0 << 0 << 4 << 0 << 7
        set2 << 3 << 5 << 8 << 13 << 8 << 5
        set3 << 5 << 6 << 7 << 3 << 4 << 5
        set4 << 9 << 7 << 5 << 3 << 1 << 2
        series3 = QtCharts.QPercentBarSeries()
        series3.append(set0)
        series3.append(set1)
        series3.append(set2)
        series3.append(set3)
        series3.append(set4)
        chart3 = QtCharts.QChart()
        chart3.addSeries(series3)
        chart3.setTitle("Percent Example")
        chart3.setAnimationOptions(QtCharts.QChart.SeriesAnimations)
        categories = ["Jan", "Feb", "Mar", "Apr", "May", "Jun"]
        axis = QtCharts.QBarCategoryAxis()
        axis.append(categories)
        chart3.createDefaultAxes()
        chart3.setAxisX(axis, series3)
        chart3.legend().setVisible(True)
        chart3.legend().setAlignment(QtCore.Qt.AlignBottom)
        self._chart_view3 = QtCharts.QChartView(chart3)
        self._chart_view3.setRenderHint(QtGui.QPainter.Antialiasing)

        widgets.verticalLayout_21.addWidget(self._chart_view3)