from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.units import cm  # This is how many point there in a cm
import os
from reportlab.platypus import Table

# Setta la working directory al path dello script
abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

c = canvas.Canvas("text.pdf", pagesize=landscape(A4), bottomup=0)
textobj = c.beginText()
textobj.setTextOrigin(cm, cm)
textobj.setFont("Helvetica", 10)

textobj.textLine("Prima riga")

data = [
    ['row0-1', 'row0-2', 'row0-3'],
    ['row1-1', 'row1-2', 'row1-3'],
    ['row2-1', 'row2-2', 'row2-3'],
    ['row3-1', 'row3-2', 'row3-3'],
    ['row4-1', 'row4-2', 'row4-3'],
    ['row5-1', 'row5-2', 'row5-3'],
    ['row6-1', 'row6-2', 'row6-3'],
]
for row in data:
    textobj.textLine(f"{row[0]} - {row[1]} - {row[2]}")
c.drawText(textobj)
c.setTitle("Text")
c.showPage()
c.save()
