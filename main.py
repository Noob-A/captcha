import time

from PyQt5 import *
from PyQt5 import QtGui, uic
from PyQt5.QtGui import QImage, QMovie
from PyQt5.QtWidgets import *
import sys


class MyDialog (QMainWindow) :
  def __init__(self) :
    super ().__init__ ()
    uic.loadUi ("test.ui", self)
    movie = QMovie("load.gif")
    self.myLabel.setMovie(movie)
    movie.start()
    self.setStyleSheet ("QMainWindow {background: 'white';}");
    time.sleep(2)
    self.myLabel.hide()
    self.pushButton.clicked.connect (self.buttonPress)

  def buttonPress(self) :
    print ("pressed!" + self.lineEdit.text())
    self.myLabel.hide()


if __name__ == '__main__' :
  app = QApplication (sys.argv)
  dialog = MyDialog ()
  dialog.show ()
  sys.exit (app.exec_ ())
