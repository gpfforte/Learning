from tkinter import ANCHOR, Tk, CENTER, NO, RIGHT, BOTTOM, Y, X, Scrollbar, LEFT
from tkinter import ttk
from random import randint, choice

ws = Tk()
ws.title('PythonGuides')
ws.geometry('500x500+50+50')
ws['bg'] = '#66ccff'

style = ttk.Style()
style.theme_use('clam')
style.configure("Mio_stile.TLabel", foreground="blue", background="yellow")
style.configure("Treeview", highlightthickness=0, bd=0,
                font=('Calibri', 11))  # Modify the font of the body
style.configure("Treeview.Heading", foreground="blue",
                background="orange", font=('Calibri', 13, 'bold'))

# print(style.theme_names())
# style.configure("Treeview.Column", foreground="blue", background="orange")


def fixed_map(option):
    # Fix for setting text colour for Tkinter 8.6.9
    # From: https://core.tcl.tk/tk/info/509cafafae
    #
    # Returns the style map for 'option' with any styles starting with
    # ('!disabled', '!selected', ...) filtered out.

    # style.map() returns an empty list for missing options, so this
    # should be future-safe.
    return [elm for elm in style.map('Treeview', query_opt=option) if
            elm[:2] != ('!disabled', '!selected')]


style.map('Treeview', foreground=fixed_map(
    'foreground'), background=fixed_map('background'))

tree_frame = ttk.Frame(ws)
tree_frame.pack()

# scrollbar
ytree_scroll = ttk.Scrollbar(tree_frame)
ytree_scroll.pack(side=RIGHT, fill=Y)

xtree_scroll = ttk.Scrollbar(tree_frame, orient='horizontal')
xtree_scroll.pack(side=BOTTOM, fill=X)
cols = ('player_id', 'player_name',
        'player_rank', 'player_states', 'player_city', 'player_score', 'player_active')
my_tree = ttk.Treeview(tree_frame, columns=cols, height=8,
                       yscrollcommand=ytree_scroll.set, xscrollcommand=xtree_scroll.set, show="headings")

ytree_scroll.config(command=my_tree.yview)
xtree_scroll.config(command=my_tree.xview)

# define our column

for col in cols:
    # Format colums
    my_tree.column(col, anchor=CENTER, width=100)
    # Create headings
    my_tree.heading(col, text=col, anchor=CENTER)

valori = (('0', 'Ninja', '101', 'Oklahoma', 'Moore', randint(0, 100), choice([True, False])),
          ('1', 'Ranger', '102', 'Wisconsin', 'Green Bay',
          randint(0, 100), choice([True, False])),
          ('2', 'Deamon', '103', 'California', 'Placentia',
          randint(0, 100), choice([True, False])),
          ('3', 'Dragon', '104', 'New York', 'White Plains',
          randint(0, 100), choice([True, False])),
          ('4', 'CrissCross', '105', 'California',
          'San Diego', randint(0, 100), choice([True, False])),
          ('5', 'ZaqueriBlack', '106', 'Wisconsin',
          'TONY', randint(0, 100), choice([True, False])),
          ('6', 'RayRizzo', '107', 'Colorado', 'Denver',
          randint(0, 100), choice([True, False])),
          ('7', 'Byun', '108', 'Pennsylvania', 'ORVISTON',
          randint(0, 100), choice([True, False])),
          ('8', 'Trink', '109', 'Ohio', 'Cleveland',
          randint(0, 100), choice([True, False])),
          ('9', 'Twitch', '110', 'Georgia', 'Duluth',
          randint(0, 100), choice([True, False])),
          ('10', 'Animus', '111', 'Connecticut', 'Hartford',
          randint(0, 100), choice([True, False])),
          ('11', 'Animus', '112', 'Connecticut', 'Hartford',
          randint(0, 100), choice([True, False])),
          )

# add data
# tags are used to change later the background color of the rows
for idx, valore in enumerate(valori):
    tag = "odd" if idx % 2 == 1 else "even"
    my_tree.insert(parent='', index='end', text='',
                   values=valore, tags=(tag,))

my_tree.pack()

my_tree.tag_configure("odd", background='#E8E8E8')
my_tree.tag_configure("even", background='#DFDFDF')


def selectItem(a):
    curItem = my_tree.focus()
    print(my_tree.item(curItem))


my_tree.bind('<ButtonRelease-1>', selectItem)
my_label = ttk.Label(ws, text="Etichetta", style="Mio_stile.TLabel")
my_label.pack(anchor="nw")

ws.mainloop()
