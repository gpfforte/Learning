from tkinter import *
import holidays
from pandas import DataFrame
from pandastable import Table




root=Tk()

my_frame=Frame(root)
my_frame.pack()
list_hol=[]
for date,name in sorted(holidays.IT(years=2021).items()):
    list_hol.append(date)
list_str=[]
for x in list_hol:
    data=x.strftime("%Y-%m-%d")
    list_str.append(data)

df = DataFrame (list_str,columns=["Data"])

pt = Table(my_frame, dataframe= df, showtoolbar=True, showstatusbar=True)
pt.show()

mask_1 = (pt.model.df["Data"] == df["Data"].max())
mask_2 = (pt.model.df["Data"] == df["Data"].min())
mask_3 = ((pt.model.df["Data"] > df["Data"].min()) & (pt.model.df["Data"] < df["Data"].max()))
pt.setColorByMask("Data", mask_1, "red")
pt.setColorByMask("Data", mask_2, "#000fff000") # or green
pt.setColorByMask("Data", mask_3, "yellow")

print(df["Data"].max())

#print (df)



root.mainloop()
##
##mask_1 = pt.model.df['A'] < 5
##
##pt.setColorByMask('A', mask_1, 'red')
##
##mask_2 = pt.model.df['A'] >= 5
##
##pt.setColorByMask('A', mask_2, 'green')
