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
        self._chart_view2 = None
        self._chart_view3 = None
        self.childrenCardsPlot = 0
        self.childrenPomoPlot = 0

    def setupConnections(self):
        widgets.qCBoxFlashcards.currentIndexChanged.connect(self.selectTopicToFlashcards)
        widgets.qCBoxPomodoro.currentIndexChanged.connect(self.selectTopicToPomodoro)
        widgets.btnPomodoroRefresh.clicked.connect(self.setupPomodoroStats)

    def setupWidgets(self):
        widgets.lblTotalTime.setText(f'00:00:00')

    def setupFlashcardsStats(self):
        print("\nSETUP FLASHCARDS ###")
        print('\n ID FLASHCARDS É O SEGUINTE: ', self.topicFlashcardsID)
        widgets.lblCardsInTotal.setText(self.loadTotalCards(topicid=self.topicFlashcardsID))
        badcount, okcount, goodcount, studedcards = self.loadFeedbacksCount(topicid=self.topicFlashcardsID)
        widgets.lblBadFeedbackCount.setText(str(badcount))
        widgets.lblOkFeedbackCount.setText(str(okcount))
        widgets.lblGoodFeedbackCount.setText(str(goodcount))
        widgets.lblStudedCards.setText(str(studedcards))
        self.loadSatisfatoryOrUnsatisfatory(topicid=self.topicFlashcardsID)
        self.setupFlashcardsPlot(badcount, okcount, goodcount)

    def setupPomodoroStats(self):   
        print('\n ID POMODORO É O SEGUINTE: ', self.topicPomodoroID)
        widgets.lblTotalPomodoros.setText(self.loadTotalPomodoros(topicid=self.topicPomodoroID))
        widgets.lblTotalTime.setText(self.loadTotalTimePomodoros(topicid=self.topicPomodoroID))
        #self.setupPomodoroPlot()

        #LOAD TABLE WITH STATUS: 
        #self.loadStatusOfDecks(topicid=self.topicID)

    ######## POMODORO

    def setupFlashcardsPlot(self, badcount, okcount, goodcount):
        oldwidget = self._chart_view2
        print("selecting...")
        series = QtCharts.QPieSeries()
        series.append('Desempenho Abaixo', badcount)
        series.append('Desempenho Ok', okcount)
        series.append('Desempenho Ótimo', goodcount)
        if badcount == 0 and okcount == 0 and goodcount == 0:
            pass
        else:
            slice2 = series.slices()[1]
            slice2.setExploded()
            slice2.setPen(QtGui.QPen(QtCore.Qt.darkGray, 0))
            slice2.setBrush(QtCore.Qt.gray)
        chart2 = QtCharts.QChart()
        chart2.addSeries(series)
        chart2.setTitle('Rendimento de Estudos: Flashcards')
        chart2.legend().show()
        self._chart_view2 = QtCharts.QChartView(chart2)
        self._chart_view2.setRenderHint(QtGui.QPainter.Antialiasing)
        self._chart_view2.chart().setTheme(QtCharts.QChart.ChartThemeDark)

        if self.childrenCardsPlot == 0:
            widgets.verticalLayout_18.removeWidget(oldwidget)
            widgets.verticalLayout_18.addWidget(self._chart_view2)
            self.childrenCardsPlot += 1
        else:
            widgets.verticalLayout_18.removeWidget(oldwidget)
            widgets.verticalLayout_18.addWidget(self._chart_view2)

    def setupPomodoroPlot(self):
        oldwidget = self._chart_view3
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
        chart3.setTitle("Rendimento de Estudos: Pomodoro")
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
        self._chart_view3.chart().setTheme(QtCharts.QChart.ChartThemeDark)

        if self.childrenPomoPlot == 0:
            widgets.verticalLayout_21.addWidget(self._chart_view3)
            self.childrenPomoPlot += 1
        else:
            widgets.verticalLayout_21.removeWidget(oldwidget)
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
        print("CURRENT INDEX: ", idx)
        if idx == -1:
            return
        elif idx == 0:    # Show geral
            self.topicFlashcardsID = -1
            self.setupFlashcardsStats()
        else:   # Show specific decks
            with DBMainOperations() as db:
                self.topicFlashcardsID = db.getAllRecords(tbl='topics', specifcols='topic_id', 
                                                          whclause=f'topic_name = "{topicname}"')[0][0]
            self.setupFlashcardsStats()
        

    def selectTopicToPomodoro(self):
        idx = widgets.qCBoxPomodoro.currentIndex()
        self.topicPomodoroName = widgets.qCBoxPomodoro.currentText()
        topicname = self.topicPomodoroName
        if idx == -1:
            return
        elif idx == 0:    # Show geral
            self.topicPomodoroID = -1
            self.setupPomodoroStats()
        else:   # Show specific decks
            with DBMainOperations() as db:
                self.topicPomodoroID = db.getAllRecords(tbl='topics', specifcols='topic_id', 
                                                          whclause=f'topic_name = "{topicname}"')[0][0]
            self.setupPomodoroStats()

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
        print("LOADING FEEDBACKS, TOPICID:", self.topicFlashcardsID)
        with DBMainOperations() as db:
            if topicid == -1:
                exist = db.cursor.execute(f"""
                            SELECT EXISTS(SELECT 1 FROM decks);"""
                        ).fetchall()[0][0]
            else:
                exist = db.cursor.execute(f"""
                            SELECT EXISTS(SELECT 1 FROM decks WHERE topic_id = {topicid});"""
                        ).fetchall()[0][0]
            existAtLeastACard = True if exist == 1 else False
            if existAtLeastACard:
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
                return badcount, okcount, goodcount, studedcards
            else:
                return 0, 0, 0, 0

    def loadSatisfatoryOrUnsatisfatory(self, topicid=-1):

        with DBMainOperations() as db:

            if topicid == -1:
                decks = db.getAllRecords(tbl='decks')
            else:
                decks = db.getAllRecords(tbl='decks', whclause=f'topic_id = {topicid}')
            satisfatory, unsatisfatory = [], []
            for deck in decks:
                if deck[2] > 50:
                    satisfatory.append((deck[1], f'{deck[2]}%'))
                else:
                    unsatisfatory.append((deck[1], f'{deck[2]}%'))
        widgets.listSatisfatoryDecks.clear()
        widgets.listUnsatisfatoryDecks.clear()
        for deck in satisfatory:
            item = QtWidgets.QListWidgetItem()
            item.setText(f'{deck[0]}, {deck[1]}')
            widgets.listSatisfatoryDecks.addItem(item)
        for deck in unsatisfatory:
            item = QtWidgets.QListWidgetItem()
            item.setText(f'{deck[0]}, {deck[1]}')
            widgets.listUnsatisfatoryDecks.addItem(item)