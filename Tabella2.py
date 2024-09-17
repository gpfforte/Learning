# Python program to create a table

from tkinter import *


class Table:

    def __init__(self, window, lista):
        # find total number of rows and
        # columns in list
        total_rows = len(lista)
        total_columns = len(lista[0])
        # code for creating table
        for i in range(total_rows):
            for j in range(total_columns):

                self.e = Entry(window, width=20, fg='black',
                               font=('Arial', 10, 'normal'))

                self.e.grid(row=i, column=j)
                self.e.insert(END, lista[i][j])


# take the data
lst = [(1, 'Raj', 'Mumbai', 19),
       (2, 'Aaryan', 'Pune', 18),
       (3, 'Vaishnavi', 'Mumbai', 20),
       (4, 'Rachna', 'Mumbai', 21),
       (5, 'Shubham', 'Delhi', 21)]


# create root window
root = Tk()
t = Table(root, lst)
root.mainloop()
