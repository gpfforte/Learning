# importing from tkinter
from random import randint, random
from tkinter import ttk, Tk, BOTH
from pandastable import Table

# variable
my_text = ["Text updated !!!", "Try Again",
           "Another Time", "You'll be more lucky"]

# function define for
# updating the my_label
# widget content


def aggiorna():
    # use global variable
    global my_text
    r = randint(0, len(my_text)-1)
    # configure
    my_label.config(text=my_text[r])


# creating the tkinter window
root = Tk()
root.title("Template")
root.geometry('1000x700+200+100')
my_frame_comandi = ttk.Frame(root)
my_frame_comandi.pack(pady=5, padx=5, fill=BOTH)
# my_frame_top = ttk.Frame(root)
# my_frame_top.pack(pady=5, padx=5, fill=BOTH)

my_notebook = ttk.Notebook(root)
my_notebook.pack(fill=BOTH, expand=1, pady=5, padx=5)

my_frame_1_inside = ttk.Frame(my_notebook)
my_notebook.add(my_frame_1_inside, text="Tab 1")

my_button_1_inside = ttk.Button(my_frame_1_inside,
                                text="Please update",
                                command=aggiorna)
#my_button_1_inside.pack(side="left", padx=5, pady=5)
my_button_1_inside.grid(column=0, row=0, sticky="NW", padx=5, pady=5)

my_button_1_inside = ttk.Button(my_frame_1_inside,
                                text="Please update",
                                command=aggiorna)
#my_button_1_inside.pack(side="left", padx=5, pady=5)
my_button_1_inside.grid(column=1, row=0, padx=5, pady=5)

my_button_1_inside = ttk.Button(my_frame_1_inside,
                                text="Please update",
                                command=aggiorna)
#my_button_1_inside.pack(side="left", padx=5, pady=5)
my_button_1_inside.grid(column=0, row=1, sticky="NW", padx=5, pady=5)

my_frame_2_inside = ttk.Frame(my_notebook)
my_notebook.add(my_frame_2_inside, text="Tab 2")

my_button_2_inside = ttk.Button(my_frame_2_inside,
                                text="Please update",
                                command=aggiorna)
# my_button_2_inside.pack(side="left", padx=5, pady=5)
my_button_2_inside.grid(column=0, row=0, sticky="NW", padx=5, pady=5)
# create a button widget and attached
# with counter function
my_button = ttk.Button(my_frame_comandi,
                       text="Please update",
                       command=aggiorna)
my_button.pack(side="left", padx=5, pady=5)
# create a Label widget
my_label = ttk.Label(my_frame_comandi,
                     text="Testo Base")
my_label.pack(side="left", padx=5, pady=5)
inside_frame = ttk.Frame(my_frame_2_inside)
inside_frame.grid(column=0, sticky="S", row=1, padx=5, pady=5)
pt = Table(inside_frame, showtoolbar=True, showstatusbar=True)

# place the widgets
# in the gui window
pt.autoResizeColumns()
pt.show()

# Start the GUI
root.mainloop()
