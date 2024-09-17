from guizero import App, Text, Box, PushButton, TextBox, info

app = App(title="Hello world", height=700, width=1000)
box_upper=Box(app, border=1, align="top", width="fill", height="fill",)
box_middle=Box(app, border=1, align="top", width="fill", height="fill")
box_lower=Box(app, border=1, align="bottom", width="fill", height="fill")

testo = Text(box_upper, text="Welcome to the app")
testo1 = Text(box_upper, text="")

button = PushButton(box_middle, command=info, args=["Info", "You pressed the button"], align="right")

def chiudi():
    app.destroy()


button = PushButton(box_lower, chiudi, text="Chiudi", align="bottom")

# client.publish("Status", payload="Lampada/On", qos=0, retain=False)





app.display()
