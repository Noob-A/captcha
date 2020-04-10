import sys
from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import Qt
import random
class Rect:
  def __init__(self, x,y,w,h) :
    self.w = w
    self.h = h
    self.y = y
    self.x = x



  def draw(self, painter):
    painter.drawRect(self.x,self.y ,self.w,self.h)

  def vsplit(self):
    rand = random.randint(70, 30)
    randd = round(100/rand)
    a = Rect(self.x,self.y,self.w/randd,self.h)
    b = Rect(self.x+self.w/rand,self.y,self.w/randd,self.h)
    return [a,b]

  def hsplit(self):
    r = random.uniform(0.3, 0.7)
    randd = r
    a = Rect(self.x, self.y, self.w, self.h*randd)
    b = Rect(self.x, self.y+a.h, self.w, self.h-a.h)
    return [a,b]

class MyDialog(QMainWindow):
  def __init__(self) :
    super().__init__()

  def paintEvent(self, event):
    painter = QPainter(self)
    painter.setPen(QPen(Qt.green, 1))
    r = []
    rr = r.hsplit()
    print(rr)




  def mousePressEvent(self, event):
    self.update()



if __name__ == '__main__':
  app = QApplication(sys.argv)
  dialog = MyDialog()
  dialog.show()
  sys.exit(app.exec_())