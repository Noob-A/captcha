import random
import sys
import math

from PyQt5 import uic
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


class Line:
  def __init__(self, x1, y1, x2, y2):
    self.x1 = min(x1,x2)
    self.y1 = min(y1, y2)
    self.x2 = max(x1, x2)
    self.y2 = max(y1, y2)

  @property
  def horizontal(self):
    return self.y1 == self.y2

  @property
  def vertical(self):
    return self.x1 == self.x2

  def contains(self, x, y):
    if self.vertical:
      return x == self.x1 and self.y1 <= y <= self.y2
    elif self.horizontal:
      return y == self.y1 and self.x1 <= x <= self.x2
    else:
      return False

  @property
  def empty(self):
    return self.x1 == self.x2 and self.y1 == self.y2

  #def __eq__(self, o) -> bool:
  #  return self.x1 == o.x1 and self.x2 == o.x2 and self.y1 == o.y1 and self.y2 == o.y2

  @property
  def length(self):
    if self.vertical:
      return abs(self.y1 - self.y2)
    elif self.horizontal:
      return abs(self.x1 - self.x2)
    else:
      return math.sqrt(pow(self.x1-self.x2, 2) + pow(self.y1-self.y2, 2))

  def get_door_line(self):
    delta = 20
    if self.length < (delta*6):
      return None

    if self.vertical:
      return Line(self.x1, (self.y1 + self.y2) / 2 - delta, self.x2, (self.y1 + self.y2) / 2 + delta)
    elif self.horizontal:
      return Line((self.x1 + self.x2) / 2 - delta, self.y1, (self.x1 + self.x2) / 2 + delta, self.y2)
    else:
      return None

  def draw(self, painter):
    painter.drawLine(self.x1, self.y1, self.x2, self.y2)

  def overlap(self, other):
    if (self.horizontal and other.vertical) or (self.vertical and other.horizontal):
      return None

    start_on_other = other.contains(self.x1, self.y1)
    end_on_other = other.contains(self.x2, self.y2)

    other_start_on_this = self.contains(other.x1, other.y1)
    other_end_on_this = self.contains(other.x2, other.y2)

    result = None

    if start_on_other and end_on_other:
      result = self
    elif other_start_on_this and other_end_on_this:
      result =  other
    elif end_on_other and other_start_on_this:
      result =  Line(other.x1, other.y1, self.x2, self.y2)
    elif start_on_other and other_end_on_this:
      result =  Line(self.x1, self.y1, other.x2, other.y2)

    if result:
      return result if not result.empty else None
    else:
      return None

class Rect:
  def __init__(self, x, y, w, h):
    self.w = w
    self.h = h
    self.y = y
    self.x = x
    self.bline = Line(x, y, x + w, y)
    self.tline = Line(x, y + h, x + w, y + h)
    self.lline = Line(x, y, x, y + h)
    self.rline = Line(x + w, y, x + w, y + h)

  def shrink(self, amount):
    return Rect(self.x + amount, self.y + amount, self.w - 2 * amount, self.h - 2 * amount)

  @property
  def lines(self):
    return [self.bline, self.tline, self.lline, self.rline]

  def draw(self, painter):
    for line in [self.bline, self.tline, self.lline, self.rline]:
      line.draw(painter)

  def vsplit(self):
    rand = random.randint(70, 30)
    randd = round(100 / rand)
    a = Rect(self.x, self.y, self.w / randd, self.h)
    b = Rect(self.x + self.w / rand, self.y, self.w / randd, self.h)
    return [a, b]

  def hsplit(self):
    randd = random.uniform(0.3, 0.7)
    a = Rect(self.x, self.y, self.w, self.h * randd)
    b = Rect(self.x, self.y + a.h, self.w, self.h - a.h)
    return [a, b]


def split(rect, acc, depth):
  if depth == 0 or (depth == 1 and random.uniform(0, 1) > 0.5):
    acc.append(rect)
    return

  horz = rect.w > rect.h
  randd = random.uniform(0.4, 0.6)
  if horz:
    a = Rect(rect.x, rect.y, int(rect.w * randd), rect.h)
    b = Rect(rect.x + a.w, rect.y, rect.w - a.w, rect.h)
  else:
    a = Rect(rect.x, rect.y, rect.w, int(rect.h * randd))
    b = Rect(rect.x, rect.y + a.h, rect.w, rect.h - a.h)

  for r in [a, b]:
    split(r, acc, depth - 1)


class MyDialog(QMainWindow):
  def __init__(self):
    super().__init__()
    self.animations = []
    uic.loadUi("painter's.ui", self)
    self.setStyleSheet("QMainWindow {background: 'white';}")

  def paintEvent(self, event):
    painter = QPainter(self)
    # painter.setPen(QPen(Qt.green, 1))
    rect = Rect(10, 10, 1200, 800)
    acc = []
    split(rect, acc, 4)
    for r in acc:
      pen = QPen()
      #color = QColor(random.randint(0,255),random.randint(0,255),random.randint(0,255))
      #pen.setColor(color)
      pen.setWidth(2)
      painter.setPen(pen)
      # shrunk = r.shrink(4)
      # shrunk.draw(painter)
      r.draw(painter)

    lines = []
    for rc in acc:
      for line in rc.lines:
        lines.append(line)

    pen = QPen()
    color = QColor(255, 255, 255)
    #color = QColor(0, 0, 0)
    pen.setColor(color)
    pen.setWidth(10)
    painter.setPen(pen)

    for line1 in lines:
      for line2 in lines:
        if line1 != line2:
          overlap = line1.overlap(line2)
          if overlap is not None:
            #overlap.draw(painter)
            door = overlap.get_door_line()
            if door is not None:
              door.draw(painter)

  def mousePressEvent(self, event):
    self.update()


if __name__ == '__main__':
  app = QApplication(sys.argv)
  dialog = MyDialog()
  dialog.show()
  sys.exit(app.exec_())
