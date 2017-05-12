import pythoncom, pyHook
from Tkinter import *

def OnMouseEvent(event):
    # called when mouse events are received
    ret = {}
    ret['MessageName'] = event.MessageName
    ret['Message'] = event.Message
    ret['Time'] = event.Time
    ret['Window'] = event.Window
    ret['WindowName'] = event.WindowName
    ret['Position'] = event.Position
    ret['Wheel'] = event.Wheel
    ret['Injected'] = event.Injected
    print ret

# return True to pass the event to other handlers
    return True

master = Tk()

def callback():
    print "click!"

b = Button(master, text="OK", command=callback)
b.pack()

mainloop()

# create a hook manager
hm = pyHook.HookManager()
# watch for all mouse events
hm.MouseAll = OnMouseEvent
# set the hook
hm.HookMouse()
# wait forever
x = pythoncom.PumpMessages()

hm.UnhookMouse()