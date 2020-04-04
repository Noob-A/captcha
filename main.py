import time

from PyQt5 import *
from PyQt5 import QtGui, uic
from PyQt5.QtCore import QTimer, QPropertyAnimation, QVariantAnimation, QEasingCurve, pyqtSlot, QVariant, QEventLoop
from PyQt5.QtGui import QImage, QMovie, QPainter, QPalette, QColor
from PyQt5.QtWidgets import *
import sys


class AnimationLabel (QLabel) :
  def __init__(self, *args, **kwargs) :
    QLabel.__init__ (self, *args, **kwargs)
    self.animation = QVariantAnimation ()
    self.animation.valueChanged.connect (self.changeColor)

  @pyqtSlot (QVariant)
  def changeColor(self, color) :
    palette = self.palette ()
    palette.setColor (QPalette.WindowText, color)
    self.setPalette (palette)

  def startFadeIn(self) :
    self.animation.stop ()
    self.animation.setStartValue (QColor (0, 0, 0, 0))
    self.animation.setEndValue (QColor (0, 0, 0, 255))
    self.animation.setDuration (2000)
    self.animation.setEasingCurve (QEasingCurve.InBack)
    self.animation.start ()

  def startFadeOut(self) :
    self.animation.stop ()
    self.animation.setStartValue (QColor (0, 0, 0, 255))
    self.animation.setEndValue (QColor (0, 0, 0, 0))
    self.animation.setDuration (2000)
    self.animation.setEasingCurve (QEasingCurve.OutBack)
    self.animation.start ()

  def startAnimation(self) :
    self.startFadeIn ()
    loop = QEventLoop ()
    self.animation.finished.connect (loop.quit)
    loop.exec_ ()
    QTimer.singleShot (2000, self.startFadeOut)


class Widget (QWidget) :
  def __init__(self) :
    super ().__init__ ()
    lay = QVBoxLayout (self)
    self.greeting_text = AnimationLabel ("greeting_text")
    self.greeting_text.setStyleSheet ("font : 45px; font : bold; font-family : HelveticaNeue-UltraLight")
    lay.addWidget (self.greeting_text)
    btnFadeIn = QPushButton ("fade in")
    btnFadeOut = QPushButton ("fade out")
    btnAnimation = QPushButton ("animation")
    lay.addWidget (btnFadeIn)
    lay.addWidget (btnFadeOut)
    lay.addWidget (btnAnimation)
    btnFadeIn.clicked.connect (self.greeting_text.startFadeIn)
    btnFadeOut.clicked.connect (self.greeting_text.startFadeOut)
    btnAnimation.clicked.connect (self.greeting_text.startAnimation)


class MyDialog (QMainWindow) :
  def __init__(self) :
    super ().__init__ ()
    uic.loadUi ("test.ui", self)
    movie = QMovie("load.gif")
    self.myLabel.setMovie(movie)
    movie.start()
    movie = QMovie ("white.gif")
    self.myLabel.setMovie (movie)
    movie.start ()
    self.setStyleSheet ("QMainWindow {background: 'white';}");
    self.pushButton.clicked.connect (self.buttonPress)

    self.pushButton.hide()
    self.lineEdit.hide()

    QTimer.singleShot(4000,
                      lambda: self.doneLoading())

  def doneLoading(self):
    self.pushButton.show()
    self.myLabel.hide()
    self.lineEdit.show()
    self.myLabel2.setStyleSheet("{background-color: rgba(255, 255, 0,255}")


  def buttonPress(self) :
    print ("pressed!" + self.lineEdit.text())
    self.myLabel.hide()





if __name__=='__main__':
    app = QApplication (sys.argv)
    dialog = MyDialog ()
    dialog.show ()
    sys.exit (app.exec_ ())
