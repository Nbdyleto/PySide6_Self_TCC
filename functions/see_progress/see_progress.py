from PySide6 import QtCore, QtGui, QtWidgets, QtCharts
from functions.db_main_operations import DBMainOperations

from functions.see_progress.ui_see_progress import Ui_SeeProgressPage
import datetime

class SeeProgressMainPage(QtWidgets.QWidget):
    def __init__(self):
        super(SeeProgressMainPage, self).__init__()
        self.ui = Ui_SeeProgressPage()
        self.ui.setupUi(self)
        self.setupVariables()
        self.setupConnections()
        self.setupWidgets()

    def setupVariables(self):
        global widgets
        widgets = self.ui
        self.topicFlashcardsID = -1
        self.topicPomodoroID = -1

    def setupConnections(self):
        widgets.qCBoxFlashcards.currentIndexChanged.connect(self.selectTopicToFlashcards)
        widgets.qCBoxPomodoro.currentIndexChanged.connect(self.selectTopicToPomodoro)
        widgets.btnPomodoroRefresh.clicked.connect(self.setupFlashcardsStats)
        widgets.btnPomodoroRefresh.clicked.connect(self.setupPomodoroStats)

    def setupWidgets(self):
        widgets.lblTotalTime.setText(f'00:00:00')

    def setupFlashcardsStats(self):
        print('\n ID FLASHCARDS É O SEGUINTE: ', self.topicFlashcardsID)
        widgets.lblCardsInTotal.setText(self.loadTotalCards(topicid=self.topicFlashcardsID))
        badcount, okcount, goodcount, studedcards = self.loadFeedbacksCount(topicid=self.topicFlashcardsID)
        widgets.lblBadFeedbackCount.setText(badcount)
        widgets.lblOkFeedbackCount.setText(okcount)
        widgets.lblGoodFeedbackCount.setText(goodcount)
        widgets.lblStudedCards.setText(studedcards)

    def setupPomodoroStats(self):   
        print('\n ID POMODORO É O SEGUINTE: ', self.topicPomodoroID)
        widgets.lblTotalPomodoros.setText(self.loadTotalPomodoros(topicid=self.topicPomodoroID))
        widgets.lblTotalTime.setText(self.loadTotalTimePomodoros(topicid=self.topicPomodoroID))

        #LOAD TABLE WITH STATUS: 
        #self.loadStatusOfDecks(topicid=self.topicID)

    def setupCharts(self):
        pass
    ######## POMODORO

    def setupFlashcardsPlot(self):
        series = QtCharts.QPieSeries()
        series.append('Desempenho Ótimo', 1)
        series.append('Desempenho Ok', 2)
        series.append('Desempenho Abaixo', 3)
        slice2 = series.slices()[1]
        slice2.setExploded()
        slice2.setLabelVisible()
        slice2.setPen(QtGui.QPen(QtCore.Qt.darkGreen, 2))
        slice2.setBrush(QtCore.Qt.green)
        chart2 = QtCharts.QChart()
        chart2.addSeries(series)
        chart2.setTitle('Simple piechart example')
        chart2.legend().show()
        self._chart_view2 = QtCharts.QChartView(chart2)
        self._chart_view2.setRenderHint(QtGui.QPainter.Antialiasing)
        widgets.verticalLayout_20.addWidget(self._chart_view2)    # verticalLayout_20: Tasks Frame

    def setupPomodoroPlot(self):
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
    
    def loadTopicsInComboBox(self):
        widgets.qCBoxPomodoro.clear()
        widgets.qCBoxFlashcards.clear()
        with DBMainOperations() as db:
            topics = db.getAllRecords(tbl='topics')
        tablerow = 0
        for row in topics:
            if row[0] == 0:
                widgets.qCBoxFlashcards.addItem('Geral')
                widgets.qCBoxPomodoro.addItem('Geral')
                continue
            widgets.qCBoxFlashcards.addItem(row[1])
            widgets.qCBoxPomodoro.addItem(row[1])
            tablerow += 1

    def selectTopicToFlashcards(self):
        idx = widgets.qCBoxFlashcards.currentIndex()
        self.topicFlashcardsName = widgets.qCBoxFlashcards.currentText()
        topicname = self.topicFlashcardsName
        if idx <= 0:    # Show geral
            self.topicFlashcardsID = -1
        else:   # Show specific decks
            with DBMainOperations() as db:
                self.topicFlashcardsID = db.getAllRecords(tbl='topics', specifcols='topic_id', 
                                                          whclause=f'topic_name = "{topicname}"')[0][0]
        self.setupFlashcardsStats()
        #self.setupFlashcardsPlot()

    def selectTopicToPomodoro(self):
        idx = widgets.qCBoxPomodoro.currentIndex()
        self.topicPomodoroName = widgets.qCBoxPomodoro.currentText()
        topicname = self.topicPomodoroName
        if idx <= 0:    # Show geral
            self.topicPomodoroID = -1
        else:   # Show specific decks
            with DBMainOperations() as db:
                self.topicPomodoroID = db.getAllRecords(tbl='topics', specifcols='topic_id', 
                                                          whclause=f'topic_name = "{topicname}"')[0][0]
        self.setupPomodoroStats()
        #self.setupPomodoroPlot()

    ########################################
    # Pomodoro Statistics Functions #####################################

    def loadTotalPomodoros(self, topicid=-1):
        with DBMainOperations() as db:
            if topicid <= 0:
                qry = """SELECT COUNT(*) FROM pomodoroProgress"""
                totalpomodoro = db.cursor.execute(qry).fetchall()[0][0]
            else:
                qry = F"SELECT COUNT(*) FROM pomodoroProgress WHERE topic_id={topicid}"
                totalpomodoro = db.cursor.execute(qry).fetchall()[0][0]
        return str(totalpomodoro)

    def loadTotalTimePomodoros(self, topicid=-1):
        with DBMainOperations() as db:
            if topicid <= 0:
                pomodoros = db.getAllRecords(tbl='pomodoroProgress', specifcols='total_time')
                print('topicos gerais', pomodoros)
            else: 
                pomodoros = db.getAllRecords(tbl='pomodoroProgress', specifcols='total_time', whclause=f'topic_id={topicid}')
                print('topico diferente tio', pomodoros)
            #totaltime = QtCore.QTime(0, 0, 0, 0)
            mysum = datetime.timedelta()
            for pomo in pomodoros:
                (h, m, s) = pomo[0].split(':')  #pomo[0] = total_time
                d = datetime.timedelta(hours=int(h), minutes=int(m), seconds=int(s))
                mysum += d
        return str(mysum)


    ########################################
    # Flashcards Statistics Functions #####################################

    def loadTotalCards(self, topicid=-1):
        totalcards = 0
        with DBMainOperations() as db:
            if topicid == -1:
                qry = """SELECT COUNT(*) FROM flashcards"""
                totalcards = db.cursor.execute(qry).fetchall()[0][0]
            else:
                qry1 = f"""SELECT deck_id FROM decks WHERE topic_id = {topicid}"""
                decksID = db.cursor.execute(qry1).fetchall()
                for deckID in decksID:
                    qry2 = f"""SELECT COUNT(*) FROM flashcards WHERE deck_id = {deckID[0]}"""
                    totalcards += db.cursor.execute(qry2).fetchall()[0][0]
        return str(totalcards)

    def loadFeedbacksCount(self, topicid=-1):
        with DBMainOperations() as db:
            if topicid == -1:
                qry1 = f"""SELECT SUM(bad_feedback) FROM decks"""
                qry2 = f"""SELECT SUM(ok_feedback) FROM decks"""
                qry3 = f"""SELECT SUM(good_feedback) FROM decks"""
                badcount = db.cursor.execute(qry1).fetchall()[0][0]
                okcount = db.cursor.execute(qry2).fetchall()[0][0]
                goodcount = db.cursor.execute(qry3).fetchall()[0][0]
                studedcards = badcount + okcount + goodcount
            else:
                qry1 = f"""SELECT bad_feedback FROM decks WHERE topic_id = {topicid}"""
                qry2 = f"""SELECT ok_feedback FROM decks WHERE topic_id = {topicid}"""
                qry3 = f"""SELECT good_feedback FROM decks WHERE topic_id = {topicid}"""
                badcount = db.cursor.execute(qry1).fetchall()[0][0]
                okcount = db.cursor.execute(qry2).fetchall()[0][0]
                goodcount = db.cursor.execute(qry3).fetchall()[0][0]
                studedcards = badcount + okcount + goodcount
        return str(badcount), str(okcount), str(goodcount), str(studedcards)
    
    def loadStatusOfDecks(self, topicid=-1):
        pass