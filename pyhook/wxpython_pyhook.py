#!/usr/bin/env python
import wx
import pyHook
from PIL import ImageGrab

# fullscreen
im=ImageGrab.grab()
im.show()
im.save('im.png', 'PNG')

# part of the screen
# im=ImageGrab.grab(bbox=(10,10,500,500))
# im.show()

def OnMouseEvent(event):
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
    return True

def OnKeyboardEvent(event):
    ret = {}
    ret['MessageName'] =event.MessageName
    ret['Message'] =event.Message
    ret['Time'] = event.Time
    ret['Window'] = event.Window
    ret['WindowName'] = event.WindowName
    ret['Ascii'] =event.Ascii, chr(event.Ascii)
    ret['Key'] =event.Key
    ret['KeyID'] =event.KeyID
    ret['ScanCode'] =event.ScanCode
    ret['Extended'] =event.Extended
    ret['Injected'] =event.Injected
    ret['Alt'] = event.Alt
    ret['Transition'] = event.Transition
    print ret
    return True

# class MyFrame(wx.Frame):
#     """ We simply derive a new class of Frame. """
#     def __init__(self, parent, title):
#         wx.Frame.__init__(self, parent, title=title, size=(200,100))
#         self.control = wx.TextCtrl(self, style=wx.TE_MULTILINE)
#         self.Show(True)
#
# app = wx.App(False)
# frame = MyFrame(None, 'Small editor')

from Tkinter import * # or(from Tkinter import Tk) on Python 2.x
root = Tk()
root.wait_visibility(root)
root.wm_attributes('-alpha',0.3)

# create a hook manager
hm = pyHook.HookManager()
# watch for all mouse events
hm.MouseAll = OnMouseEvent
hm.KeyAll = OnKeyboardEvent
# set the hook
hm.HookMouse()
hm.HookKeyboard()

# app.MainLoop()
root.mainloop()
