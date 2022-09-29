from PySide6.QtCore import *
from PySide6.QtWidgets import *
from PySide6.QtGui import *

SECONDS_TOTAL = 60

class CircularProgress(QWidget):
        def __init__(self):
                QWidget.__init__(self)

                self.m_second_format = ''

                # Custom Properties
                self.value = 100
                self.text = ''
                self.width = 300
                self.height = 300
                self.progress_width = 6
                self.progress_rounded_cap = False
                self.progress_color = '#44475a'
                self.max_value = 100
                self.font_family = 'Segoe UI'
                self.font_size = 15
                self.text_color = '#f8f8f2'
                self.enable_shadow = True
                self.text = F'{SECONDS_TOTAL//60:02d}:{SECONDS_TOTAL%60:02d}'

                # SET DEFAULT SIZE WITHOUT LAYOUT
                self.resize(self.width, self.height)

        # PAINT EVENT (DESIGN YOUR CIRCULAR PROGRESS)
        def paintEvent(self, event):
                width = self.width - self.progress_width
                height = self.height - self.progress_width
                margin = self.progress_width / 2
                value = self.value * 360 / self.max_value

                outerRadius = min(self.width, self.height)
                baseRect = QRectF(1, 1, outerRadius - 2, outerRadius - 2)

                # PAINTER
                
                paint = QPainter()
                paint.begin(self)
                paint.setRenderHint(QPainter.Antialiasing) # remove pixelazed edges
                paint.setFont(QFont(self.font_family, self.font_size))
                
                # CREATE RECTS
                seconds_rect = QRect(0, 0, self.width, self.height)
                paint.setPen(Qt.NoPen)
                paint.drawRect(seconds_rect)

                pomodoros_rect = QRect(0, 10, self.width, self.height)
                paint.setPen(Qt.NoPen)
                paint.drawRect(pomodoros_rect)

                # PEN
                pen = QPen()
                
                pen.setColor(QColor(self.progress_color))
                pen.setWidth(self.progress_width)

                # Set Round Cap
                if self.progress_rounded_cap:
                        pen.setCapStyle(Qt.RoundCap)
                # CREATE ARC / CIRCULAR PROGRESS
                paint.setPen(pen)
                paint.drawArc(margin, margin, width, height, -90*16, -value*16)
                
                # CREATE TEXT
                pen.setColor(QColor(self.text_color))

                paint.setPen(pen)
                paint.drawText(seconds_rect, Qt.AlignCenter, f'{self.text}')

                #self.drawBase(paint, baseRect)

                # END
                paint.end()


        def set_value(self, value):
                self.value = value
                self.repaint()

        def drawBase(self, p, baseRect):
                #elif bs == self.StyleLine:
                self.outlinePenWidth = 0.5

                p.setBrush(Qt.NoBrush)
                p.drawEllipse(baseRect.adjusted(self.outlinePenWidth/1, self.outlinePenWidth/1, -self.outlinePenWidth/1, -self.outlinePenWidth/1))