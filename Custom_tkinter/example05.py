import customtkinter

app = customtkinter.CTk()
tabview = customtkinter.CTkTabview(app)
tabview.pack(padx=20, pady=20)

tab_1 = tabview.add("tab 1")
tab_2 = tabview.add("tab 2")
tabview.set("tab 2")

button_1 = customtkinter.CTkButton(tab_2)
button_1.pack(padx=20, pady=20)


app.mainloop()
