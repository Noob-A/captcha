import sys

from PyQt5 import uic, QtGui
from PyQt5.QtCore import QTimer, QPropertyAnimation, QSize
from PyQt5.QtGui import QMovie, QPixmap, QPainter
from PyQt5.QtWidgets import *
import sys
from PyQt5.QtGui import *

######################################################################################################

class MyDialog (QMainWindow) :
  def __init__(self) :
    super ().__init__ ()
    uic.loadUi ("test.ui", self)
    movie = QMovie("load.gif")
    self.myLabel.setMovie(movie)
    movie.start()
    self.setStyleSheet ("QMainWindow {background: 'white';}")
    self.pushButton.clicked.connect (self.buttonPress)

    self.pushButton.hide()
    self.lineEdit.hide()
    self.pushButton.setIcon (QtGui.QIcon("buton.gif"))
    self.pushButton.setIconSize (QSize (1000, 1500))

    QTimer.singleShot(4000,
                      lambda: self.doneLoading())

  def fade(self, widget) :
    self.effect = QGraphicsOpacityEffect ()
    widget.setGraphicsEffect (self.effect)

    self.animation = QPropertyAnimation (self.effect, b"opacity")
    self.animation.setDuration (1000)
    self.animation.setStartValue (1)
    self.animation.setEndValue (0)
    self.animation.start ()

  def unfade(self, widget) :
    self.effect = QGraphicsOpacityEffect ()
    widget.setGraphicsEffect (self.effect)
    self.animation = QPropertyAnimation (self.effect, b"opacity")
    self.animation.setDuration (3000)
    self.animation.setStartValue (0)
    self.animation.setEndValue (1)
    self.animation.start ()

  def doneLoading(self):
    self.pushButton.show()
    self.myLabel.hide()
    self.lineEdit.show()
    self.unfade (self.pushButton)
    self.setStyleSheet ("QMainWindow {background: rgba(246, 246, 246, 255)}")




  def buttonPress(self) :
    print ("pressed!" + self.lineEdit.text())
    self.myLabel.hide()


if __name__=='__main__':
    app = QApplication (sys.argv)
    dialog = MyDialog ()
    dialog.show ()
    sys.exit (app.exec_ ())


