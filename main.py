import math
import os
import sys

import clipboard
from PyQt5 import uic
from PyQt5.QtCore import QTimer, QPropertyAnimation, QSize
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from _winapi import *
import pyautogui #for ctrl+v
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
    self.pushButton_3.clicked.connect(self.copy)
    self.pushButton_2.clicked.connect(self.symbol_of_c)
    self.km.clicked.connect(self.km1)
    self.money.clicked.connect(self.money)

    self.money.hide()
    self.pushButton.hide()
    self.pushButton_3.hide()
    self.pushButton_2.hide()
    self.km.hide()
    self.lineEdit.hide()

    self.celciusAction_2.triggered.connect(self.celcius_menu_action)
    # self.fahrenheitAction.triggered.connect(self.faringate_menu_action)

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
    i = self.lineEdit.text()

    if i.endswith('°') :
      i = i[:-1]
      c = float(i)
      f = (c * (9 / 5)) + 32
      f = math.floor(f)
      self.lineEdit.setText(f"{c}°C ({f}°F)")
    if i.endswith('KM'):
      i = i[:-2]
      c = float(i)
      mi = c * 0.62137
      f = round(mi)
      self.lineEdit.setText(f"{c}KM ({f}miles)")


  def symbol_of_c(self):
    n = self.lineEdit.text()
    self.lineEdit.setText(f"{n}°")

  def copy(self):
    # pyautogui.move(0,-350)
    # #dobleclick
    # pyautogui.click()
    # pyautogui.click()
    # pyautogui.click()
    # pyautogui.hotkey('ctrl', 'c')  # Press the Ctrl-C hotkey combination.
    clipboard.copy(self.lineEdit.text())
  def km1(self):
    n = self.lineEdit.text()
    self.lineEdit.setText(f"{n}KM")
    self.myLabel.hide()

  def unf(self, widget) :
    self.effect = QGraphicsOpacityEffect()
    widget.setGraphicsEffect(self.effect)
    self.animation = QPropertyAnimation(self.effect, b"opacity")
    self.animation.setDuration(3000)
    self.animation.setStartValue(0)
    self.animation.setEndValue(1)
    self.animation.start()

  def money(self):
    pass

  def doneLoading(self) :
    self.pushButton.show()
    self.pushButton_2.show()
    self.pushButton_3.show()
    self.km.show()
    self.setStyleSheet("QMainWindow {background: rgba(247, 247, 239 ,255)}")
    self.setStyleSheet("QMainWindow {background: hsl(60, 33, 95)}")
    self.myLabel.hide()
    self.lineEdit.show()
    self.unfade(self.pushButton)
    self.unfade(self.lineEdit)
    self.unfade(self.pushButton_2)
    self.unfade(self.pushButton_3)
    self.unfade(self.km)
    self.unfade(self.money)
    self.setStyleSheet("QLineEdit { border-radius: 5px; }")


  def celcius_menu_action(self) :
    pass




if __name__ == '__main__' :
  app = QApplication(sys.argv)
  dialog = MyDialog()
  dialog.show()
  sys.exit(app.exec_())
