from tkinter import *

class EntryFormat(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.createWidgets()

    def createWidgets(self):
        sv = StringVar()
        data = Entry(self, textvariable=sv)
        sv.trace("w", lambda name, index, mode, sv=sv: 
                             entryUpdateData(data))
        data.pack()

def entryUpdateData(entry):
    text = entry.get()
    if len(text) in (4,7):
        entry.insert(END,'-')
        entry.icursor(len(text)+1)
    elif len(text) not in (0,5,8):
        if not text[-1].isdigit():
            entry.delete(0,END)
            entry.insert(0,text[:-1])
    if len(text) > 10:
        entry.delete(0,END)
        entry.insert(0,text[:8])


