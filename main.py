import sys

from PyQt5 import uic
from PyQt5.QtCore import QTimer, QPropertyAnimation, QSize
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

######################################################################################################
far = False
cel = False


class MyDialog(QMainWindow) :

  def __init__(self) :
    super().__init__()
    self.animations = []
    uic.loadUi("test.ui", self)
    movie = QMovie("load.gif")
    self.myLabel.setMovie(movie)
    movie.start()
    self.setStyleSheet("QMainWindow {background: 'white';}")
    self.pushButton.clicked.connect(self.buttonPress)
    self.pushButton.hide()
    self.lineEdit.hide()

    self.celciusAction.triggered.connect(self.celcius_menu_action)
    self.fahrenheitAction.triggered.connect(self.faringate_menu_action)

    self.pushButton.setIconSize(QSize(1000, 1500))
    QTimer.singleShot(4000,
                      lambda : self.doneLoading())

  def fade(self, widget) :
    self.effect = QGraphicsOpacityEffect()
    widget.setGraphicsEffect(self.effect)

    animation = QPropertyAnimation(self.effect, b"opacity")
    animation.setDuration(1000)
    animation.setStartValue(1)
    animation.setEndValue(0)
    animation.start()
    self.animations.append(animation)

  def unfade(self, widget) :
    self.effect = QGraphicsOpacityEffect()
    widget.setGraphicsEffect(self.effect)
    animation = QPropertyAnimation(self.effect, b"opacity")
    animation.setDuration(3000)
    animation.setStartValue(0)
    animation.setEndValue(1)
    animation.start()
    self.animations.append(animation)

  def buttonPress(self) :
    input = self.lineEdit.text()
    if (far) :
      Fahrenheit = (input * 9 / 5) + 32
      back = "weather"

    self.myLabel.hide()

  def unf(self, widget) :
    self.effect = QGraphicsOpacityEffect()
    widget.setGraphicsEffect(self.effect)
    self.animation = QPropertyAnimation(self.effect, b"opacity")
    self.animation.setDuration(3000)
    self.animation.setStartValue(0)
    self.animation.setEndValue(1)
    self.animation.start()

  def doneLoading(self) :
    self.pushButton.show()
    self.setStyleSheet("QMainWindow {background: rgba(247, 247, 239 ,255)}")
    self.setStyleSheet("QMainWindow {background: hsl(60, 33, 95)}")
    self.myLabel.hide()
    self.lineEdit.show()
    self.unfade(self.pushButton)
    self.unfade(self.lineEdit)
    self.setStyleSheet("QLineEdit { border-radius: 5px; }")




  def faringate_menu_action(self) :
    far = True
    self.lineEdit.setText("°")
    # self.lbl.setText(self.qle.text()) label from input

  def celcius_menu_action(self) :
    cel = True
    self.lineEdit.setText("°")


if __name__ == '__main__' :
  app = QApplication(sys.argv)
  dialog = MyDialog()
  dialog.show()
  sys.exit(app.exec_())
