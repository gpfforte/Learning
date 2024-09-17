from random import randint, random
from tkinter import ttk, Tk, BOTH, Listbox, END, StringVar, messagebox, ANCHOR
import requests
import json
import datetime as dt
import pytz
import sys
import os

# Setta la working directory al path dello script
abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

api_key = os.environ.get("API_KEY_OPENWEATHERMAP")

tz = pytz.timezone('Europe/Rome')


def geocode(city):
    # http://api.openweathermap.org/geo/1.0/direct?q={city name},{state code},{country code}&limit={limit}&appid={API key}

    api_request = requests.get(
        f"http://api.openweathermap.org/geo/1.0/direct?q={city[0]},{city[1]}&limit=5&appid={api_key}")
    # print(api)
    return json.loads(api_request.content)


def cerca_meteo():
    # use global variable
    global localita
    global scelta_nazione
    global my_listbox
    my_listbox.delete(0, END)

    city = localita.get()
    if len(city) < 3:
        messagebox.showinfo("Errore Località",
                            "Scrivi almeno 3 caratteri", parent=root)
        return
    nazione = scelta_nazione.get()
    api = geocode([city, nazione])
    if api:
        if len(api) > 1:
            if 'state' in api[0]:
                my_listbox.insert(
                    END, f"Dati per la prima occorrenza di {len(api)} - {api[0]['name']} - {api[0]['country']} - {api[0]['state']}")
            else:
                my_listbox.insert(
                    END, f"Dati per la prima occorrenza di {len(api)} - {api[0]['name']} - {api[0]['country']}")
        else:
            if 'state' in api[0]:
                my_listbox.insert(
                    END, f"Unica occorrenza - {api[0]['name']} - {api[0]['country']} - {api[0]['state']}")
            else:
                my_listbox.insert(
                    END, f"Unica occorrenza - {api[0]['name']} - {api[0]['country']}")

        lat = api[0]["lat"]
        lon = api[0]["lon"]
        api_request = requests.get(
            f"https://api.openweathermap.org/data/2.5/onecall?lat={lat}&lon={lon}&appid={api_key}&units=metric")
        api = json.loads(api_request.content)
        # Time is the number of seconds from EPOCH (1 Gennaio 1970)
        utc_time_current = dt.datetime.utcfromtimestamp(
            api['current']['dt'])

        local_time_current = pytz.utc.localize(
            utc_time_current, is_dst=None).astimezone(tz).strftime('%Y-%m-%d %H:%M:%S')

        utc_time_sunrise = dt.datetime.utcfromtimestamp(
            api['current']['sunrise'])
        local_time_sunrise = pytz.utc.localize(
            utc_time_sunrise, is_dst=None).astimezone(tz).strftime('%Y-%m-%d %H:%M:%S')

        utc_time_sunset = dt.datetime.utcfromtimestamp(
            api['current']['sunset'])
        local_time_sunset = pytz.utc.localize(
            utc_time_sunset, is_dst=None).astimezone(tz).strftime('%Y-%m-%d %H:%M:%S')

        my_listbox.insert(END, f"Latitudine: \t {lat}")
        my_listbox.insert(END, f"Longitudine: \t {lon}")
        my_listbox.insert(
            END, f"Current Time: \t {local_time_current} (utc) {utc_time_current}")

        my_listbox.insert(
            END, f"Current Time: \t {local_time_current} (utc) {utc_time_current}")
        my_listbox.insert(
            END, f"Surise Time: \t {local_time_sunrise} (utc) {utc_time_sunrise}")
        my_listbox.insert(
            END, f"Sunset Time: \t {local_time_sunset} (utc) {utc_time_sunset}")
        my_listbox.insert(END, f"Temperature: \t {api['current']['temp']} °C")
        my_listbox.insert(
            END, f"Pressure: \t {api['current']['pressure']} hPa")
        my_listbox.insert(END, f"Humidity: \t {api['current']['humidity']} %")
        my_listbox.insert(
            END, f"Wind Speed: \t {api['current']['wind_speed']} Km/h")
        my_listbox.insert(END, f"Wind Dir: \t {api['current']['wind_deg']} °")
        my_listbox.insert(END,
                          f"Description: \t {api['current']['weather'][0]['description'].title()}")
    else:
        messagebox.showinfo("Errore Ricerca",
                            "Non è stato trovato nulla", parent=root)


# creating the tkinter window
root = Tk()
root.title("Geocoding & Weather Api")
root.geometry('1000x700+100+100')


my_notebook = ttk.Notebook(root)
my_notebook.pack(fill=BOTH, expand=1, pady=5, padx=5)

my_frame_1_inside = ttk.Frame(my_notebook)
my_notebook.add(my_frame_1_inside, text="Condizioni Meteo")
# create a Label widget

my_frame_comandi = ttk.Frame(my_frame_1_inside)
my_frame_comandi.grid(pady=5, padx=5, sticky='nw')

my_label = ttk.Label(my_frame_comandi,
                     text="Scrivi località e cerca meteo")
my_label.grid(row=0, column=0,  sticky="NW", padx=5, pady=5)


localita = StringVar()

my_entry_località = ttk.Entry(my_frame_comandi, textvariable=localita)
my_entry_località.grid(row=1, column=0, sticky="NW", padx=5, pady=5)
label_nazione = ttk.Label(my_frame_comandi, text="Nazione")
label_nazione.grid(row=1, column=1, sticky="NW", padx=5, pady=5)
scelta_nazione = StringVar()
combo_nazione = ttk.Combobox(
    my_frame_comandi, textvariable=scelta_nazione, values=["IT", "DE", "GB"], width=10, state="readonly")
combo_nazione.grid(row=1, column=2, sticky="NW", padx=5, pady=5)
combo_nazione.current(newindex=0)
my_button_1_inside = ttk.Button(my_frame_comandi,
                                text="Cerca meteo",
                                command=cerca_meteo)
#my_button_1_inside.pack(side="left", padx=5, pady=5)
my_button_1_inside.grid(row=2, column=0,  sticky="NW", padx=5, pady=5)


def select(event):
    print(my_listbox.get(ANCHOR))


my_listbox = Listbox(my_frame_1_inside, font="Monokai", width=50, height=20)
my_listbox.grid(row=3, column=0, sticky="NW", padx=5, pady=5)
my_listbox.bind("<ButtonRelease-1>", select)
# my_listbox.insert(END, "Prova")

# Start the GUI
root.mainloop()
