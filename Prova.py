# Import the required libraries
from tkinter import *
from tkinter import ttk

# Create an instance of tkinter frame
win = Tk()

# Set the size of the tkinter window
win.geometry("700x350")
s = ttk.Style()
s.theme_use('clam')

# Configure the style of Heading in Treeview widget
s.configure('Treeview.Heading', background="green3")

# Add a Treeview widget
tree = ttk.Treeview(win, column=("c1", "c2"), show='headings', height=8)
tree.column("# 1", anchor=CENTER)
tree.heading("# 1", text="ID")
tree.column("# 2", anchor=CENTER)
tree.heading("# 2", text="FName")

# Insert the data in Treeview widget
tree.insert('', 'end', text="1", values=('1', 'Honda'))
tree.insert('', 'end', text="2", values=('2', 'Hundayi'))
tree.insert('', 'end', text="3", values=('3', 'Tesla'))
tree.insert('', 'end', text="4", values=('4', 'Wolkswagon'))
tree.insert('', 'end', text="5", values=('5', 'Tata'))
tree.insert('', 'end', text="6", values=('6', 'Renault'))
tree.insert('', 'end', text="7", values=('7', 'Audi'))
tree.insert('', 'end', text="8", values=('8', 'BMW'))

tree.pack()

win.mainloop()
