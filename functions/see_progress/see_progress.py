from PySide6 import QtCore, QtGui, QtWidgets, QtCharts
from functions.db_main_operations import DBMainOperations

from functions.see_progress.ui_see_progress import Ui_SeeProgressPage

class SeeProgressMainPage(QtWidgets.QWidget):
    def __init__(self):
        super(SeeProgressMainPage, self).__init__()
        self.ui = Ui_SeeProgressPage()
        self.ui.setupUi(self)
        self.setupVariables()
        self.setupConnections()
        self.setupWidgets()
        self.getTotalTime()
        self.setupCharts()

    def setupVariables(self):
        global widgets
        widgets = self.ui
        self.topicID = -1

    def setupConnections(self):
        widgets.qCBoxFlashcards.currentIndexChanged.connect(self.selectTopicInComboBox)

    def setupWidgets(self):
        widgets.lblTotalTime.setText(f'00:00:00')

    def setupStatsInWidgets(self):
        widgets.lblCardsInTotal.setText(self.loadTotalCards(topicid=self.topicID))
        #widgets.lblStudedCards.setText(self.loadTotalStudedCards(topicid=self.topicID))
        badcount, okcount, goodcount, studedcards = self.loadFeedbacksCount(topicid=self.topicID)
        widgets.lblBadFeedbackCount.setText(badcount)
        widgets.lblOkFeedbackCount.setText(okcount)
        widgets.lblGoodFeedbackCount.setText(goodcount)
        widgets.lblStudedCards.setText(studedcards)
        
        #LOAD TABLE WITH STATUS: 
        #self.loadStatusOfDecks(topicid=self.topicID)

    def setupCharts(self):
        widgets.lblTotalPomodoros = 0
        widgets.lblTotalTime = 0
    
    ######## POMODORO

    def getTotalTime(self):
        with DBMainOperations() as db:
            pomodoros = db.getAllRecords(tbl='pomodoroProgress')
            #totaltime = QtCore.QTime(0, 0, 0, 0)
            tothours, totmins, totsecs = 0, 0, 0
            # pomo[0] = pomo_id
            # pomo[1] = completed
            # pomo[2] = study_date
            # pomo[3] = total_time
            # pomo[4] = topic_id
            for pomo in pomodoros:
                pomosplit = pomo[3].split(':')
                tothours += int(pomosplit[0])
                totmins += int(pomosplit[1])
                totsecs += int(pomosplit[2])
                #qpomo = QtCore.QTime(int(hours), int(mins), int(secs))
        print('')
        print(f'{tothours}:{totmins}:{totsecs}')
            
    """

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
    """

    def loadTopicsInComboBox(self):
        widgets.qCBoxFlashcards.clear()
        with DBMainOperations() as db:
            topics = db.getAllRecords(tbl='topics')
        tablerow = 0
        for row in topics:
            if row[0] == 0:
                widgets.qCBoxFlashcards.addItem('Geral')
                continue
            widgets.qCBoxFlashcards.addItem(row[1])
            tablerow += 1
    
    def selectTopicInComboBox(self):
        idx = widgets.qCBoxFlashcards.currentIndex()
        self.topicName = widgets.qCBoxFlashcards.currentText()
        topicname = self.topicName
        if idx == 0:    # Show geral
            self.topicID = -1
        else:   # Show specific decks
            with DBMainOperations() as db:
                self.topicID = db.getAllRecords(tbl='topics', specifcols='topic_id', whclause=f'topic_name = "{topicname}"')[0][0]
        self.setupStatsInWidgets()
    
    ########################################
    # Statistics Functions #####################################

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