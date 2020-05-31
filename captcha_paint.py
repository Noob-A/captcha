import random
import sys
import math
import threading
from enum import Enum
from threading import Thread
from typing import List, Any

from PyQt5 import uic, QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from flags import Flags


class Facing(Flags):
    South = 1
    SouthWest = 2
    West = 4
    NorthWest = 8
    North = 16
    NorthEast = 32
    East = 64
    SouthEast = 128

class RoomType:
  def __init__(self, name_rus: str, min_size: float, recommended_facing):
      self.recommended_facing = recommended_facing
      self.min_size = min_size
      self.name_rus = name_rus

class RoomTypes:
  Unknown = RoomType("Неизвестный тип", 0, Facing.__no_flags_name__)
  Bedroom = RoomType("Спальная", 12, Facing.East | Facing.SouthEast)
  MasterBedroom = RoomType("Мастер спальня", 20, Facing.East | Facing.SouthEast)
  Bathroom = RoomType("Ванная комната", 8, Facing.NorthEast)
  LivingRoom = RoomType("Гостиная", 25, Facing.South)
  Kitchen = RoomType("Кухня", 10, Facing.SouthEast)
  BoilerRoom = RoomType("Бойлерная", 6, Facing.North)
  GuestRoom = RoomType("Гостевая", 15, Facing.East | Facing.SouthEast)
  Toilet = RoomType("Санузел", 2, Facing.NorthEast)
  Pantry = RoomType("Постирочная", 5, Facing.NorthEast)
  Terrace = RoomType("Терасса", 5, Facing.South)
  Wardrobe = RoomType("Гардероб", 12, Facing.NorthEast)
  Storage = RoomType("Хранилище", 5, Facing.West)


class Line:
  def __init__(self, x1, y1, x2, y2):
    self.x1 = min(x1, x2)
    self.y1 = min(y1, y2)
    self.x2 = max(x1, x2)
    self.y2 = max(y1, y2)

  @property
  def q(self):
    return QLine(self.x1, self.y1, self.x2, self.y2)

  @property
  def horizontal(self):
    return self.y1 == self.y2

  @property
  def is_vert_or_horz(self):
    return self.x1 == self.x2 or self.y1 == self.y2

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
  def center(self) -> QPointF:
    return QPointF((self.x1 + self.x2) / 2, (self.y1 + self.y2) / 2)

  @property
  def empty(self):
    return self.x1 == self.x2 and self.y1 == self.y2

  # def __eq__(self, o) -> bool:
  #  return self.x1 == o.x1 and self.x2 == o.x2 and self.y1 == o.y1 and self.y2 == o.y2

  @property
  def length(self):
    if self.vertical:
      return abs(self.y1 - self.y2)
    elif self.horizontal:
      return abs(self.x1 - self.x2)
    else:
      return math.sqrt(pow(self.x1 - self.x2, 2) + pow(self.y1 - self.y2, 2))

  def get_door_line(self):
    delta = 20
    if self.length < (delta * 6):
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
      result = other
    elif end_on_other and other_start_on_this:
      result = Line(other.x1, other.y1, self.x2, self.y2)
    elif start_on_other and other_end_on_this:
      result = Line(self.x1, self.y1, other.x2, other.y2)

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
    self.doors = []

  @property
  def center(self):
    return QPointF(self.x + self.w / 2, self.y + self.h / 2)

  def shrink(self, amount):
    return Rect(self.x + amount, self.y + amount, self.w - 2 * amount, self.h - 2 * amount)

  @property
  def qrectf(self):
    return QRectF(self.x, self.y, self.w, self.h)

  @property
  def lines(self):
    return [self.bline, self.tline, self.lline, self.rline]

  def draw(self, painter: QPainter):
    for line in [self.bline, self.tline, self.lline, self.rline]:
      line.draw(painter)
    flags = QTextOption()
    flags.setAlignment(Qt.AlignCenter)
    painter.drawText(self.qrectf,
                     f'{self.area / 10000} m²\n{self.w / 100}×{self.h / 100}', flags)


  def getThisRoomType(self):

  @property
  def area(self):
    return self.w * self.h

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


def split(rect, acc, depth, total_depth):
  if depth == 0 or (random.uniform(0, 1) > 0.8):
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
    split(r, acc, depth - 1, total_depth)


class MyDialog(QMainWindow):
  requiredRooms = [
    RoomTypes.Bedroom,
    RoomTypes.Bedroom,
    RoomTypes.MasterBedroom,
    RoomTypes.GuestRoom,
    RoomTypes.Toilet,
    RoomTypes.Bathroom,
    RoomTypes.BoilerRoom,
    RoomTypes.Pantry,
    RoomTypes.Terrace,
    RoomTypes.Wardrobe
  ]

  def __init__(self):
    super().__init__()
    # self.animations = []
    # uic.loadUi("painter's.ui", self)
    self.setStyleSheet("QMainWindow {background: 'white';}")

  def mousePressEvent(self, event):
    self.update()

  def hacks(self):
    while self.l:
      self.update()

  def paintEvent(self, event):
    painter = QPainter(self)
    f = QFont("Arial", pointSize=20)
    painter.setFont(f)
    # painter.setPen(QPen(Qt.green, 1))
    rect = Rect(0, 0, 1800, 1300)
    windowSize: QSize = self.size()
    v_scale = windowSize.height() / rect.h
    h_scale = windowSize.width() / rect.w
    scale = min(h_scale, v_scale)
    painter.scale(scale, scale)

    acc = []
    while (len(acc) != len(MyDialog.requiredRooms)) :
      acc.clear()
      split(rect, acc, 4, 4)
      print(f"acc:{len(acc)}, roomsNeeded:{len(MyDialog.requiredRooms)}")

    for r in acc:
      whitePen = QPen()
      # color = QColor(random.randint(0,255),random.randint(0,255),random.randint(0,255))
      # pen.setColor(color)
      whitePen.setWidth(2)
      painter.setPen(whitePen)
      shrunk = r.shrink(4)
      shrunk.draw(painter)
      # r.draw(painter)

    lines = []

    for rc in acc:
      for line in rc.lines:
        lines.append(line)

    whitePen = QPen()
    white = QColor(255, 255, 255)
    gray = QColor(128, 128, 128)
    whitePen.setColor(white)
    whitePen.setWidth(10)

    grayPen = QPen()
    grayPen.setColor(gray)
    grayPen.setWidth(2)
    if (len(acc) == len(MyDialog.requiredRooms)) :
      self.globalMatchOfNumberOfRooms = 1
    else:
      self.globalMatchOfNumberOfRooms = 0
    # this is a sucky idea because we don't know where the rooms are
    for rc1 in acc:
      for rc2 in acc:
        for line1 in rc1.lines:
          for line2 in rc2.lines:
            if line1 != line2:
              overlap = line1.overlap(line2)
              if overlap is not None:
                # overlap.draw(painter)
                door = overlap.get_door_line()
                if door is not None:
                  rc1.doors.append(door)
                  rc2.doors.append(door)
                  painter.setPen(grayPen)
                  painter.drawLine(door.center, rc1.center)
                  painter.drawLine(door.center, rc2.center)
                  painter.setPen(whitePen)
                  door.draw(painter)

    green = QColor(0, 0, 255)
    greenPen = QPen()
    greenPen.setColor(green)

    for rc in acc:
      if len(rc.doors) > 1:
        for door1 in rc.doors:
          for door2 in rc.doors:
            if door1 != door2:
              line = Line(door1.center.x(), door1.center.y(),
                          door2.center.x(), door2.center.y())
              if not line.is_vert_or_horz:
                painter.setPen(greenPen)
                # painter.drawLine(line.q)



if __name__ == '__main__':
  app = QApplication(sys.argv)
  dialog = MyDialog()
  dialog.show()
  sys.exit(app.exec_())
