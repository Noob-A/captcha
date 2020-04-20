import sys

from PyQt5.QtCore import QPropertyAnimation
from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5 import uic
import random
import time


class Line :
  def __init__(self, x1, y1, x2, y2) :
    self.x1 = x1
    self.y1 = y1
    self.x2 = x2
    self.y2 = y2


class Rect :
  def __init__(self, x, y, w, h) :
    self.w = w
    self.h = h
    self.y = y
    self.x = x
    self.bline = Line(x, y, x + w, y)
    self.tline = Line(x, y + h, x + w, y + h)
    self.lline = Line(x, y, x, y + h)
    self.rline = Line(x + w, y, x + w, y + h)


  def draw(self, painter) :
    for pt in [self.bline, self.tline, self.lline, self.rline] :
      painter.drawLine(pt.x1, pt.y1, pt.x2, pt.y2)
    # painter.drawRect(self.x,self.y ,self.w,self.h)

  def vsplit(self) :
    rand = random.randint(70, 30)
    randd = round(100 / rand)
    a = Rect(self.x, self.y, self.w / randd, self.h)
    b = Rect(self.x + self.w / rand, self.y, self.w / randd, self.h)
    return [a, b]

  def hsplit(self) :
    randd = random.uniform(0.3, 0.7)
    a = Rect(self.x, self.y, self.w, self.h * randd)
    b = Rect(self.x, self.y + a.h, self.w, self.h - a.h)
    return [a, b]

  def erase_intersection(self, line1, line2) :
    if (line1.x1 == line1.x2 and
        line1.x2 == line2.x1 and
        line2.x1 == line2.x2) :
      pass

  def get_pixel_colour(i_x, i_y, linesX, linesY) :
    import PIL.ImageGrab
    return PIL.ImageGrab.grab().load()[i_x, i_y],

  @property
  def all_lines(self) :
    return [self.bline, self.tline, self.lline, self.rline]


def split(rect, acc, depth) :
  if depth == 0 or (depth == 1 and random.uniform(0, 1) > 0.5) :
    acc.append(rect)
    return

  horz = rect.w > rect.h
  randd = random.uniform(0.3, 0.7)
  if horz :
    a = Rect(rect.x, rect.y, rect.w * randd, rect.h)
    b = Rect(rect.x + rect.w * randd, rect.y, rect.w - a.w, rect.h)
  else :
    a = Rect(rect.x, rect.y, rect.w, rect.h * randd)
    b = Rect(rect.x, rect.y + a.h, rect.w, rect.h - a.h)

  for r in [a, b] :
    split(r, acc, depth - 1)


class MyDialog(QMainWindow) :
  def __init__(self) :
    super().__init__()
    self.animations = []
    uic.loadUi("painter's.ui", self)
    movie = QMovie("load.gif")
    self.myLabel.setMovie(movie)
    movie.start()
    self.setStyleSheet("QMainWindow {background: 'white';}")
    movie.stop()
    self.myLabel.hide()
    self.pushButton.clicked.connect(self.paintEvent)

  def iterAllItems(self) :
    items = []
    for index in range(QListWidget.count()) :
      items.append(QListWidget.item(index))
    for r in items:
      self.unfade(r)


  def paintEvent(self, event) :
    painter = QPainter(self)
    # painter.setPen(QPen(Qt.green, 1))
    rect = Rect(10, 10, 600, 400)
    acc = []
    split(rect, acc, 4)

    lines = []
    for r in acc :
      lines.extend(r.all_lines)

    r.draw(painter)

  def unfade(self, widget) :
    self.effect = QGraphicsOpacityEffect()
    widget.setGraphicsEffect(self.effect)
    animation = QPropertyAnimation(self.effect, b"opacity")
    animation.setDuration(3000)
    animation.setStartValue(0)
    animation.setEndValue(1)
    animation.start()
    self.animations.append(animation)

  def mousePressEvent(self, event) :
    self.update()


if __name__ == '__main__' :
  app = QApplication(sys.argv)
  dialog = MyDialog()
  dialog.show()
  sys.exit(app.exec_())
