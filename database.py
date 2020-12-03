from tkinter import *
from PIL import ImageTk, Image
from tkinter import messagebox
from tkinter import filedialog
import sqlite3

root = Tk()
root.title("Learning Python")
root.iconbitmap("Images/Icona.ico")
root.geometry("400x600")

# Create or connect a database
# conn=sqlite3.connect('address_book.db')

# Create cursor
# cursor=conn.cursor()
'''
cursor.execute(""" CREATE TABLE addresses(
                first_name text,
                last_name text,
                address text,
                city text,
                state text,
                zipcode integer
                )""")
"""
'''


def save():
    conn = sqlite3.connect('address_book.db')
    cursor = conn.cursor()

    conn = sqlite3.connect('address_book.db')
    cursor = conn.cursor()
    record_id = select_box.get()

    cursor.execute("""UPDATE addresses SET
        first_name=:first,
        last_name=:last,
        address=:address,
        city=:city,
        state=:state,
        zipcode=:zipcode
        WHERE oid =:oid""",
                   {
                       'first': f_name_editor.get(),
                       'last': l_name_editor.get(),
                       'address': address_editor.get(),
                       'city': city_editor.get(),
                       'state': state_editor.get(),
                       'zipcode': zipcode_editor.get(),
                       'oid': record_id
                   }

                   )

    conn.commit()
    conn.close()
    editor.destroy()


def edit():
    #Capisco se è stato selezionato un numero intero, altrimenti la query va in errore

    record_id = select_box.get()
    integer=1
    try:
        int(record_id)
    except Exception as ex:
        integer=0
    try:
        if record_id > "" and integer:

            conn = sqlite3.connect('address_book.db')

            # Create cursor
            cursor = conn.cursor()
            record_id = select_box.get()

            cursor.execute("SELECT * FROM addresses WHERE oid=" + record_id)
            records = cursor.fetchall()  # one --- many ---
            if records.__len__()==1:
                global editor
                editor = Tk()
                editor.title("Update a Record")
                editor.iconbitmap("Images/Icona.ico")
                editor.geometry("400x600")

                # Loop thru results

                global f_name_editor
                global l_name_editor
                global address_editor
                global city_editor
                global state_editor
                global zipcode_editor

                # Entry
                f_name_editor = Entry(editor, width=30)
                f_name_editor.grid(row=0, column=1, padx=20, pady=(10, 0))

                l_name_editor = Entry(editor, width=30)
                l_name_editor.grid(row=1, column=1)

                address_editor = Entry(editor, width=30)
                address_editor.grid(row=2, column=1)

                city_editor = Entry(editor, width=30)
                city_editor.grid(row=3, column=1)

                state_editor = Entry(editor, width=30)
                state_editor.grid(row=4, column=1)

                zipcode_editor = Entry(editor, width=30)
                zipcode_editor.grid(row=5, column=1)

                # Label

                f_name_label_editor = Label(editor, text="First Name")
                f_name_label_editor.grid(row=0, column=0, pady=(10, 0))

                l_name_label_editor = Label(editor, text="Last Name")
                l_name_label_editor.grid(row=1, column=0)

                address_label_editor = Label(editor, text="Address")
                address_label_editor.grid(row=2, column=0)

                city_label_editor = Label(editor, text="City")
                city_label_editor.grid(row=3, column=0)

                state_label_editor = Label(editor, text="State")
                state_label_editor.grid(row=4, column=0)

                zipcode_label_editor = Label(editor, text="Zipcode")
                zipcode_label_editor.grid(row=5, column=0)

                for record in records:
                    f_name_editor.insert(0, record[0])
                    l_name_editor.insert(0, record[1])
                    address_editor.insert(0, record[2])
                    city_editor.insert(0, record[3])
                    state_editor.insert(0, record[4])
                    zipcode_editor.insert(0, record[5])

                # Create Save Button
                save_btn = Button(editor, text="Save Record", command=save)
                save_btn.grid(row=6, column=0, columnspan=2, pady=10, padx=10, ipadx=137)
            else:
                messagebox.showinfo("Errore update", "Non esiste alcun record con id = "+record_id)
        else:
            messagebox.showinfo("Errore update", "Seleziona un record id valido")
    except Exception as ex:
        messagebox.showinfo("Errore nell'update", ex)

def delete():
    record_id = select_box.get()
    integer = 1
    try:
        int(record_id)
    except Exception as ex:
        integer = 0
    try:
        if record_id > "" and integer:
            conn = sqlite3.connect('address_book.db')
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM addresses WHERE oid=" + record_id)
            records = cursor.fetchall()  # one --- many ---
            if records.__len__()==1:
                cursor.execute("DELETE FROM addresses WHERE oid=" + record_id
                           )
            else:
                messagebox.showinfo("Errore update", "Non esiste alcun record con id = " + record_id)

            conn.commit()
            conn.close()

    except Exception as ex:
        messagebox.showinfo("Errore nella cancellazione", ex)


def add():
    if f_name.get() > "":
        try:
            # Create or connect a database
            conn = sqlite3.connect('address_book.db')
            # Create cursor
            cursor = conn.cursor()
            cursor.execute("INSERT INTO addresses VALUES (:f_name,:l_name,:address,:city,:state,:zipcode)",
                           {
                               'f_name': f_name.get(),
                               'l_name': l_name.get(),
                               'address': address.get(),
                               'city': city.get(),
                               'state': state.get(),
                               'zipcode': zipcode.get()
                           })
            f_name.delete(0, END)
            l_name.delete(0, END)
            address.delete(0, END)
            city.delete(0, END)
            state.delete(0, END)
            zipcode.delete(0, END)
            conn.commit()
            conn.close()
        except Exception as ex:
            messagebox.showinfo("Errore nell'inserimento", ex)
    else:
        messagebox.showinfo("Errore nell'inserimento", "Il last name deve essere popolato")

def query():
    # Create or connect a database
    conn = sqlite3.connect('address_book.db')

    # Create cursor
    cursor = conn.cursor()

    cursor.execute("SELECT *, oid FROM addresses")
    records = cursor.fetchall()  # one --- many ---
    # print(records)
    print_records = ''
    for record in records:
        print_records += str(record[0] + " " + str(record[1]) + " " + str(record[6]) + "\n")

    query_label = Label(root, text=print_records)
    query_label.grid(row=12, column=0, columnspan=2)
    conn.commit()

    conn.close()


# Entry
f_name = Entry(root, width=30)
f_name.grid(row=0, column=1, padx=20, pady=(10, 0))

l_name = Entry(root, width=30)
l_name.grid(row=1, column=1)

address = Entry(root, width=30)
address.grid(row=2, column=1)

city = Entry(root, width=30)
city.grid(row=3, column=1)

state = Entry(root, width=30)
state.grid(row=4, column=1)

zipcode = Entry(root, width=30)
zipcode.grid(row=5, column=1)

select_box = Entry(root, width=30)
select_box.grid(row=9, column=1)

# Label

f_name_label = Label(root, text="First Name")
f_name_label.grid(row=0, column=0, pady=(10, 0))

l_name_label = Label(root, text="Last Name")
l_name_label.grid(row=1, column=0)

address_label = Label(root, text="Address")
address_label.grid(row=2, column=0)

city_label = Label(root, text="City")
city_label.grid(row=3, column=0)

state_label = Label(root, text="State")
state_label.grid(row=4, column=0)

zipcode_label = Label(root, text="Zipcode")
zipcode_label.grid(row=5, column=0)

select_box_label = Label(root, text="Select ID")
select_box_label.grid(row=9, column=0)

# Create Submit Button
add_btn = Button(root, text="Add record to database", command=add)
add_btn.grid(row=6, column=0, columnspan=2, pady=10, padx=10, ipadx=100)

# Create Query Button
query_btn = Button(root, text="Show Records", command=query)
query_btn.grid(row=7, column=0, columnspan=2, pady=10, padx=10, ipadx=137)

# Create Delete Button
delete_btn = Button(root, text="Delete Record", command=delete)
delete_btn.grid(row=10, column=0, columnspan=2, pady=10, padx=10, ipadx=137)

# Create Update Button
edit_btn = Button(root, text="Edit Record", command=edit)
edit_btn.grid(row=11, column=0, columnspan=2, pady=10, padx=10, ipadx=137)

# conn.commit()

# conn.close()


root.mainloop()
