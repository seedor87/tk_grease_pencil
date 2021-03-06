from Tkinter import *
import tkFileDialog
from tkinter.colorchooser import *
from PIL import ImageTk, ImageGrab, Image
import os

# TOOLS
LINE, RECTANGLE, CIRCLE, ARC, TEXT, FREE, ARRAY, GRID, UNDO, SAVE, COLOR = list(range(11))

# path to background image
path = os.path.join('.', 'MTRAINIER.jpg')
# path = os.path.join('.', 'MTDENALI.jpg')

# history stack
HISTORY = list()
DRAW_WIDTH = 3

root = Tk()

class ARCpopupWindow(object):
    def __init__(self,master):
        top=self.top=Toplevel(master)
        self.tkvar = StringVar(root)
        choices = {'arc', 'chord', 'pieslice'}
        self.tkvar.set('pieslice')  # set the default option
        self.popupMenu = OptionMenu(top, self.tkvar, *choices)
        Label(top, text="Choose a dish").pack()
        self.popupMenu.pack()
        self.b=Button(top,text='Ok',command=self.cleanup)
        self.b.pack()

    def cleanup(self):
        self.value = self.tkvar.get()
        self.top.destroy()

class popupWindow(object):
    def __init__(self,master):
        top=self.top=Toplevel(master)
        self.l=Label(top,text="Enter Your Text Here")
        self.l.pack()
        self.e=Entry(top)
        self.e.pack()
        self.b=Button(top,text='Ok',command=self.cleanup)
        self.b.pack()

    def cleanup(self):
        self.value=self.e.get()
        self.top.destroy()

class Paint:
    def __init__(self, canvas):
        self.canvas = canvas
        self._tool, self._obj = None, None
        self.lastx, self.lasty = None, None
        self.canvas.bind('<Button-1>', self.update_xy)
        self.canvas.bind('<B1-Motion>', self.draw)

        self.canvas_image = None
        self.FILL = 'black'

        self.file_opt = options = {}
        options['defaultextension'] = '.jpg'
        options['filetypes'] = [('all files', '.*'), ('text files', '.txt'), ('jpg files', '*.jpg')]
        options['initialdir'] = 'C:\\Users\\Bob S\\PycharmProjects\\tk_grease_pencil'
        options['initialfile'] = 'myfile.txt'
        options['parent'] = root
        options['title'] = 'This is a title'

        menubar = Menu(root)

        # create a pulldown menu, and add it to the menu bar
        filemenu = Menu(menubar, tearoff=0)
        filemenu.add_command(label="Open", command=self.set_background)
        filemenu.add_command(label="Save", command=hello)
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=root.quit)
        menubar.add_cascade(label="File", menu=filemenu)

        # create more pulldown menus
        editmenu = Menu(menubar, tearoff=0)
        editmenu.add_command(label="Cut", command=hello)
        editmenu.add_command(label="Copy", command=hello)
        editmenu.add_command(label="Paste", command=hello)
        menubar.add_cascade(label="Edit", menu=editmenu)

        helpmenu = Menu(menubar, tearoff=0)
        helpmenu.add_command(label="About", command=hello)
        menubar.add_cascade(label="Help", menu=helpmenu)

        # display the menu
        root.config(menu=menubar)

    def draw(self, event):
        if self._tool is None or self._obj is None:
            return
        x, y = self.lastx, self.lasty
        if self._tool in (LINE, RECTANGLE, CIRCLE, ARC, TEXT, GRID, UNDO, SAVE, COLOR):
            self.canvas.coords(self._obj, (x, y, event.x, event.y))
        if self._tool == ARRAY:
            self._obj = self.canvas.create_line((x, y, event.x, event.y), fill=self.FILL, width=1, smooth=True)
            HISTORY.append(self._obj)
        elif self._tool == FREE:
            self._obj = self.canvas.create_line((x, y, event.x, event.y), fill=self.FILL, width=DRAW_WIDTH, smooth=True)
            self.lastx, self.lasty = event.x, event.y
            HISTORY.append(self._obj)

    def set_background(self):
        path = tkFileDialog.askopenfilename(**self.file_opt)
        img = Image.open(path)
        img = ImageTk.PhotoImage(img)
        self.canvas.itemconfig(self.canvas, image=img)

    def update_xy(self, event):
        if self._tool is None:
            return
        x, y = event.x, event.y
        if self._tool == LINE:
            self._obj = self.canvas.create_line((x, y, x, y), fill=self.FILL, width=DRAW_WIDTH)
            HISTORY.append(self._obj)
        if self._tool == RECTANGLE:
            self._obj = self.canvas.create_rectangle((x, y, x, y), fill=self.FILL, width=DRAW_WIDTH)
            HISTORY.append(self._obj)
        if self._tool == CIRCLE:
            self._obj = self.canvas.create_oval((x, y, x, y), fill=self.FILL, width=DRAW_WIDTH)
            HISTORY.append(self._obj)
        if self._tool == ARC:
            self._obj = self.canvas.create_arc(x, y, x, y, fill=self.FILL, width=DRAW_WIDTH)
            self.w = ARCpopupWindow(self.canvas)
            self.canvas.wait_window(self.w.top)
            self.canvas.itemconfig(self._obj, style=self.w.value)
            HISTORY.append(self._obj)
        if self._tool == TEXT:
            self._obj = self.canvas.create_text(x, y, fill=self.FILL, )
            self.w = popupWindow(self.canvas)
            self.canvas.wait_window(self.w.top)
            self.canvas.itemconfig(self._obj, text=self.w.value)
            HISTORY.append(self._obj)
        if self._tool == GRID:
            height = self.canvas.winfo_height()
            width = self.canvas.winfo_width()
            for i in range(10):
                # horizontal
                self.canvas.create_line((width / 10) * i, 0, (width / 10) * i, height, fill='red')
                # verticle
                self.canvas.create_line(0, (height / 10) * i, width, (height / 10) * i, fill='red')
        if self._tool == UNDO:
            try:
                act = HISTORY.pop()
                self.canvas.delete(act)
            except IndexError as e:
                print e
        if self._tool == SAVE:
            x=root.winfo_rootx()+self.canvas.winfo_x()
            y=root.winfo_rooty()+self.canvas.winfo_y()
            x1=x+self.canvas.winfo_width()
            y1=y+self.canvas.winfo_height()
            ImageGrab.grab().crop((x,y,x1,y1)).save("out.png")
        elif self._tool == COLOR:
            color = askcolor()
            self.FILL = color[1]

        self.lastx, self.lasty = x, y


    def select_tool(self, tool):
        print('Tool', tool)
        self._tool = tool

class Tool:
    def __init__(self, whiteboard, parent=None):
        self.whiteboard = whiteboard

        frame = Frame(parent)
        self._curr_tool = None
        for i, (text, t) in enumerate((('Line', LINE), ('Rect', RECTANGLE), ('Circ', CIRCLE), ('Arc', ARC), ('Text', TEXT), ('Free', FREE), ('Array', ARRAY), ('Grid', GRID), ('Undo', UNDO), ('SAVE', SAVE), ('Color', COLOR))):
            lbl = Label(frame, text=text, width=5, relief='raised')
            lbl._tool = t
            lbl.bind('<Button-1>', self.update_tool)
            lbl.pack(padx=6, pady=6*((i+1) % 2), anchor='nw')
        frame.pack(side='left', fill='both', expand=False, anchor='w')

    def update_tool(self, event):
        lbl = event.widget
        if self._curr_tool:
            self._curr_tool['relief'] = 'raised'
        lbl['relief'] = 'sunken'
        self._curr_tool = lbl
        self.whiteboard.select_tool(lbl._tool)

def hello():
    print 'hello'


canvas = Canvas(highlightbackground='black')
whiteboard = Paint(canvas)
tool = Tool(whiteboard)
canvas.pack(fill='both', expand=True, padx=6, pady=6, anchor='w')

img = Image.open(path)
img = ImageTk.PhotoImage(img)
Paint.canvas_image = canvas.create_image((0, 0), image=img, anchor="nw")
w, h = img.width(), img.height()
canvas.config(width=w, height=h)

root.mainloop()