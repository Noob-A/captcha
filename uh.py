import time
import keyboard
import pyautogui
x=0
time.sleep(4)
while (x!=55):
  keyboard.add_hotkey('esc', lambda : exit())
  pyautogui.click(button='right')
  pyautogui.move(10,120)
  pyautogui.click()
  pyautogui.keyDown('enter')
  pyautogui.keyUp('enter')
  pyautogui.move(-10, -120)
  x += 1
