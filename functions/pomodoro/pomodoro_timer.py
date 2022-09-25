from collections import UserString, namedtuple
from PySide6 import QtCore, QtGui, QtWidgets
from PySide6.QtCore import QObject, QTimer, Signal

from functions.pomodoro.circular_progress import SECONDS_TOTAL

from .settings import STATE_POMODORO, STATE_BREAK, STATE_LONG_BREAK

class State(UserString):
    def __init__(self, seq: object, time: int):
        self.time = time
        super().__init__(seq)

TimerStatus = namedtuple('TimerStatus', 'pomodoros state')


class PomodoroTimer(QObject):

    onStart = Signal(TimerStatus)
    onStop = Signal(TimerStatus)
    onStateChange = Signal(TimerStatus)
    onChange = Signal(TimerStatus)
    finished = Signal(TimerStatus)

    def __init__(self, settings):
        super().__init__()

        self.settings = settings
        self.tickTime = 64 # ms

        self.reset()

    def getStatus(self):
        return TimerStatus(self.pomodoros, self.state)

    def reset(self):
        self.pomodoros = 0
        self.stateName = None
        self.maxSeconds = None

        self.createTimer()
        self.changeState()
    
    def createTimer(self):
        if hasattr(self, 'timer'):
            self.timer.timeout.disconnect()
        self.timer = QTimer()
        self.timer.setInterval(self.tickTime)
        self.timer.timeout.connect(self.tick)

    def changeState(self):
        if self.state is None:
            self._states = self._statesGen()
        self.stateName = next(self._states)
        self.seconds = self.state.time
        print('changing state!')

    @property
    def state(self):
        if self.stateName is None:
            return None
        time = getattr(self.settings, self.stateName)
        return State(self.stateName, time)

    def _statesGen(self):
        while True:
            yield STATE_POMODORO
            yield STATE_LONG_BREAK if self._isTimeForLongBreak() else STATE_BREAK

    def _isTimeForLongBreak(self):
        if self.pomodoros == 0:
            return False
        return self.isSetComplete() and (self.pomodoros % self.settings.repeat == 0)

    def isSetComplete(self):
        return self.state == STATE_POMODORO

    @property
    def running(self):
        return self.timer.isActive()

    @property
    def seconds(self):
        return max(0, getattr(self, '_seconds', 0))

    @seconds.setter
    def seconds(self, val):
        self._seconds = val
        self.maxSeconds = val

    @property
    def progress(self):
        return int(100 - (self.seconds / self.state.time * 100))

    @QtCore.Slot(name='tick')
    def tick(self):
        self.applyTick()

        if self.seconds <= 0:
            if self.isSetComplete():
                self.pomodoros += 1
            self.changeState()
            print("timer is over")

    def applyTick(self):
        self._seconds -= self.tickTime / 100

    def stop(self):
        self.timer.stop()
        print("stop")

    def start(self):
        self.timer.start()

    def abort(self):
        if not self.isSetComplete():
            self.changeState()
        self.stop()
        self.resetTime()
        print('aborting')

    def resetTime(self):
        self.seconds = 0

    #################
    
    def getUpper(self):
        min, sec = int(self.seconds // 60), int(self.seconds % 60)
        return f'{min:02d}:{sec:02d}'

    @property
    def progress(self):
        """Return a value to 'plot' in 'Circular Progress Bar' based on actual progress"""
        return int(100 - (self.seconds / SECONDS_TOTAL * 100))

    ########################
    