from tkinter import *

class EntryFormat():

    def __init__(self, master=None, **kw):
        sv = StringVar()
        self.entry = Entry(master, textvariable=sv)
        sv.trace("w", lambda name, index, mode, sv=sv: self.entryUpdateData(self.entry))

    def entryUpdateData(self, entry):
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

