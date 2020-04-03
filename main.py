from appJar import gui
import time as t
import ctypes
user32 = ctypes.windll.user32
# each list of numbers contains the top left x/y and bottom right x/y
screensize = user32.GetSystemMetrics(0),user32.GetSystemMetrics(1)

with gui('noob', screensize, stretch='both', sticky='news') as app:
    app.label('lal', bg='purple')
    app.setPadding([100,100])
    app.setInPadding([10,10])

app.go()




