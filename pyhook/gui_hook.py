from Tkinter import *
import threading
import pythoncom, pyHook
from multiprocessing import Pipe
import Queue
import functools

"""
http://stackoverflow.com/questions/37909484/tkinter-text-entry-with-pyhook-hangs-gui-window
"""

class TestingGUI:
    def __init__(self, root, queue, quitfun):
        self.root = root
        self.root.title('TestingGUI')
        self.queue = queue
        self.quitfun = quitfun

        self.button = Button(root, text="Withdraw", command=self.hide)
        self.button.grid()

        self.search = StringVar()
        self.searchbox = Label(root, textvariable=self.search)
        self.searchbox.grid()

        self.root.bind('<<pyHookKeyDown>>', self.on_pyhook)
        self.root.protocol("WM_DELETE_WINDOW", self.on_quit)

        self.hiding = False

    def hide(self):
        if not self.hiding:
            print 'hiding'
            self.root.withdraw()
            # instead of time.sleep + self.root.deiconify()
            self.root.after(2000, self.unhide)
            self.hiding = True

    def unhide(self):
        self.root.deiconify()
        self.hiding = False

    def on_quit(self):
        self.quitfun()
        self.root.destroy()

    def on_pyhook(self, event):
        if not queue.empty():
            scancode, ascii = queue.get()
            print scancode, ascii
            if scancode == 82:
                self.hide()

            self.search.set(ascii)

def quitfun():
    pwrite.send('quit')

def hook_loop(root, pipe):
    while 1:
        msg = pipe.recv()

        if type(msg) is str and msg == 'quit':
            print 'exiting hook_loop'
            break

        root.event_generate('<<pyHookKeyDown>>', when='tail')

# functools.partial puts arguments in this order
def keypressed(pipe, queue, event):
    queue.put((event.ScanCode, chr(event.Ascii)))
    pipe.send(1)
    print queue
    return True

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
    return True

def OnKeyboardEvent(event):
    print 'MessageName:',event.MessageName
    print 'Message:',event.Message
    print 'Time:',event.Time
    print 'Window:',event.Window
    print 'WindowName:',event.WindowName
    print 'Ascii:', event.Ascii, chr(event.Ascii)
    print 'Key:', event.Key
    print 'KeyID:', event.KeyID
    print 'ScanCode:', event.ScanCode
    print 'Extended:', event.Extended
    print 'Injected:', event.Injected
    print 'Alt', event.Alt
    print 'Transition', event.Transition
    print '---'
    return True

root = Tk()

pread, pwrite = Pipe(duplex=False)
queue = Queue.Queue()

t = threading.Thread(target=hook_loop, args=(root, pread))
t.start()

hm = pyHook.HookManager()
hm.MouseAll = OnMouseEvent
hm.HookMouse()
hm.HookKeyboard()
hm.KeyDown = functools.partial(keypressed, pwrite, queue)

TestingGUI = TestingGUI(root, queue, quitfun)
root.mainloop()