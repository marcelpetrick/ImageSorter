from tkinter import *
from os import *
import os
from PIL import ImageTk, Image
from tkinter import filedialog, messagebox

NO_DIR = 0
EMPTY_DIR = 1

class ImageSorter(object):

    def defaultValues(self):
        self.lblDir.configure(text = '...')
        self.filenames = []
        self.index = -1
        self.frmImg.configure(image = self.blackground)
        self.setBtnState('disabled')
        
    def formatCheck(self, file):
        for format in self.formats.get().split(';'):
            if format in file and len(format) > 0:
                return True
        return False

    def setDir(self):
        try:
            self.dir = filedialog.askdirectory()
            if self.dir == '':
                raise Exception(NO_DIR)
        
            self.lblDir.configure(text = self.dir)
            self.filenames = list(filter(self.formatCheck, listdir(self.dir)))
            if len(self.filenames) == 0:
                raise Exception(EMPTY_DIR)

            self.index = 0
            self.updateImage()
            self.setBtnState('normal')

        except Exception as e:
            if e.args[0] == NO_DIR:
                messagebox.showinfo('Message', 'No dir choosed.')
            elif e.args[0] == EMPTY_DIR:
                messagebox.showinfo('Message', self.dir + ' is empty.')
            else:
                messagebox.showinfo('Error', 'Problem with: ' + e.args[0])        
            self.defaultValues()

    def previous(self):
        try:
            self.index -= 1
            if self.index < 0:
                self.index = len(self.filenames) - 1
            self.updateImage()
        except Exception as e:
            messagebox.showinfo('Error', 'Problem with: ' + e.args[0])

    def next(self):
        try:
            self.index += 1
            self.overMaxIndex()
            self.updateImage()
        except Exception as e:
            messagebox.showinfo('Error', 'Problem with: ' + e.args[0])

    def trash(self):
        try:
            if not os.path.isdir(self.dir + '/trash'):
                os.mkdir(self.dir + '/trash')
                    
            filename = self.filenames[self.index]
            os.rename(self.dir + '/' + filename, self.dir + '/trash/' + filename)
            self.filenames = list(filter(self.formatCheck, listdir(self.dir)))
            if len(self.filenames) == 0:
                messagebox.showinfo('Message', self.dir + ' is empty.')
                self.defaultValues()
                return

            self.overMaxIndex()
            self.updateImage()
        except Exception as e:
            messagebox.showinfo('Error', 'Problem with: ' + e.args[0])

    def overMaxIndex(self):
        if self.index >= len(self.filenames):
            self.index = 0
    
    def updateImage(self):
        load = Image.open(self.dir + '/' + self.filenames[self.index])
        HeightDivideByWidth = load.size[1] / load.size[0]
        if HeightDivideByWidth < self.size[1] / self.size[0]:
            width = self.size[0]
            height = int(HeightDivideByWidth * self.size[0])
        else:
            height = self.size[1]
            width = int(self.size[1] / HeightDivideByWidth)
        self.img = ImageTk.PhotoImage(load.resize((width, height)))
        self.frmImg.configure(image = self.img)

    def setBtnState(self, state):
        self.btnLeft['state'] = state
        self.btnDelete['state'] = state
        self.btnRight['state'] = state
        
    def __init__(self):
        self.window = Tk()
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()
        
        self.window.geometry(str(screen_width) + 'x' + str(screen_height))
        self.size = (screen_width, int(0.8 * screen_height))
        self.index = -1
        
        self.frmHeader = LabelFrame(self.window)
        self.frmHeader.grid(row = 0)
        self.lblFormats = Label(self.frmHeader, text = 'Searched for:')
        self.lblFormats.grid(row = 0, column = 0, padx = 10)
        self.formats = StringVar(value = 'jpg;png')
        self.txtFormats = Entry(self.frmHeader, textvariable = self.formats)
        self.txtFormats.grid(row = 0, column = 1, padx = 10)
        self.btnDir = Button(self.frmHeader, text = 'Directory:', command = self.setDir)
        self.btnDir.grid(row = 0, column = 2)
        self.lblDir = Label(self.frmHeader, text = '...')
        self.lblDir.grid(row = 0, column = 3)

        self.blackground = ImageTk.PhotoImage(Image.open('blackground.png').resize(self.size))
        self.frmImg = Label(self.window, image = self.blackground)
        self.frmImg.grid(row = 1)

        self.frmButtons = Label(self.window)
        self.btnLeft = Button(self.frmButtons, text = '<', command = self.previous)
        self.btnLeft.grid(row = 0, column = 0, ipadx = int(0.15 * screen_width), ipady = 10)
        self.btnDelete = Button(self.frmButtons, text = 'Delete', command = self.trash)
        self.btnDelete.grid(row = 0, column = 1, ipadx = int(0.15 * screen_width), ipady = 10)
        self.btnRight = Button(self.frmButtons, text = '>', command = self.next)
        self.btnRight.grid(row = 0, column = 2, ipadx = int(0.15 * screen_width), ipady = 10)
        self.frmButtons.grid(row = 2)
        self.setBtnState('disabled')
        
        self.window.mainloop()

iD = ImageSorter()
