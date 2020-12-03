from tkinter import *
from PIL import ImageTk, Image
from tkinter import messagebox
from tkinter import filedialog
import requests
import json


root=Tk()
root.title("Learning Python")
root.iconbitmap("Images/Icona.ico")
root.geometry("600x100")


def zipLookup():
    #zip_en.get()
    #zipLabel=Label(root, text=zip_en.get())
    #zipLabel.grid(row=3, column=0, columnspan=2)
    

#https://www.airnowapi.org/aq/observation/zipCode/current/?format=application/json&zipCode=88901&distance=10&API_KEY=6B0A8550-1046-498A-8484-E719E488FE88

    try:
        api_request= requests.get("https://www.airnowapi.org/aq/observation/zipCode/current/?format=application/json&zipCode="+zip_en.get()+"&distance=10&API_KEY=6B0A8550-1046-498A-8484-E719E488FE88")
        api=json.loads(api_request.content)
        city = api[0]["ReportingArea"]
        quality= api[0]["AQI"]
        category= api[0]["Category"]["Name"]

        if category=="Good":
            weather_color="#0C0"#verde
        elif category == "Moderate":
            weather_color="#FFF00"#giallo
        elif category == "Unhealthy for Sensitive Groups":
            weather_color="#ff9900"
        elif category == "Unhealthy":
            weather_color="#FF000"
        elif category == "Very Unhealthy":
            weather_color="#990066"
        elif category == "Hazardous":
            weather_color="#660000"

        mylabel=Label(root, text=city+" Air Quality "+str(quality)+" "+category, font=("Helvetica",20), background=weather_color)
        mylabel.grid(row=2, column=0,columnspan=2)
        root.configure(background=weather_color)    
        
    except Exception as e:
        api = "Error..."

zip_en=Entry(root)
zip_en.grid(row=0, column=0, stick=W+E+N+S)

zip_btn=Button(root, text= "Look up Zip Code", command=zipLookup)
zip_btn.grid(row=0, column=1, stick=W+E+N+S)

root.mainloop()
