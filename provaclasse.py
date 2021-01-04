from tkinter import *
import Entryformat2

root = Tk()
a = Entryformat2.EntryFormat(master=root)
a.entry.grid(row=0, column=0)

b = Entryformat2.EntryFormat(master=root)
b.entry.grid(row=1, column=0)

root.mainloop()
