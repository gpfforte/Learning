from itertools import count
import tkinter as tk
from tkinter import ttk, Button
from tkinter.messagebox import showinfo
from random import choice

cities = ("Imperia", "Bordighera", "Alassio", "Ventimiglia", "Vallecrosia")
months = ("Jan", "Feb", "Mar", "Apr", "May")


def create_tree(win):
    def selectItem(a):
        # print(a)
        curItem = tree.focus()
        # print(tree.item(curItem))

    def item_selected(event):
        # print(event)
        for selected_item in tree.selection():
            item = tree.item(selected_item)
            record = item['values']
            # print("record", record)
            # message = ""
            # for single_value in record:
            #     print("single_value", single_value)
            #     message = f"{message}{single_value},"
            # # show a message and get rid of the last comma
            # showinfo(title='Information', message=message[:-1])
        # tree.bind('<ButtonRelease-1>', selectItem)
    columns = ("number", "month", "location")
    tree = ttk.Treeview(win, columns=columns,
                        show="tree headings", height=20, selectmode="browse")  # browse let select one item only
    # tree["columns"] = ("date", "time", "loc")
    # for column in columns:
    #     tree.column(column, width=100)
    tree.column("number", width=200, anchor=tk.CENTER)
    tree.column("month", width=200, anchor=tk.W)
    tree.column("location", width=200, anchor=tk.W)

    tree.heading("number", text="#", anchor=tk.CENTER)
    tree.heading("month", text="Month", anchor=tk.W)
    tree.heading("location", text="Location", anchor=tk.W)

    tree.bind('<<TreeviewSelect>>', item_selected)

    tree.grid(row=0, column=0, sticky='nsew')
    # add a scrollbar
    scrollbar = ttk.Scrollbar(win, orient=tk.VERTICAL, command=tree.yview)
    tree.configure(yscroll=scrollbar.set)
    scrollbar.grid(row=0, column=1, sticky='ns')
    tree.tag_configure("oddrow", background='white')
    tree.tag_configure("evenrow", background='lightblue')
    tree.tag_configure("children", background='lightgreen')

    global conteggio

    conteggio = 0

    for i in range(10):
        if conteggio % 2 == 0:
            tag = ("evenrow",)
        else:
            tag = ("oddrow",)
        tree.insert("", tk.END, text="Name", values=(
            i, choice(months), choice(cities)), tag=tag)
        conteggio += 1

    for i in range(4):
        tree.insert("I004", tk.END, text="Under I004", values=(
            f"3-{i}", choice(months), choice(cities)), tag=("children",))
    return tree


def change_city(tree):
    selected = tree.focus()
    # print("selected", selected)
    if selected:
        temp = tree.item(selected, 'values')
        tree.set(selected, column="location", value=choice(cities))
        # tree.item(selected, values=(temp[0], temp[1], choice(cities)))


def apply_style():
    style = ttk.Style()
    style.theme_use("default")  # alt clam classic
    style.configure('Emergency.TButton', font='helvetica 24', foreground='red',
                    background='yellow', padding=10)
    style.configure('Treeview',
                    background='#D3D3D3',
                    rowheight=25,
                    fieldbackground='#D3D3D3')
    style.map('Treeview', background=[('selected', '#324a6e')])
    style.map('Emergency.TButton',
              foreground=[('pressed', 'blue'),
                          ('active', 'yellow')],
              background=[('pressed', 'green'),
                          ('active', 'red')])


def main():
    root = tk.Tk()

    root.title("Gestione Tree")
    root.geometry('1000x700+200+100')

    tree = create_tree(root)

    ttk.Button(root, text='Change City', command=lambda: change_city(tree)).grid(
        row=1, column=0, sticky='we')
    ttk.Button(root, text='Close', command=root.destroy, style='Emergency.TButton').grid(
        row=2, column=0, sticky='we')

    apply_style()
    # style.map("Treeview")
    root.mainloop()


if __name__ == "__main__":
    main()
