from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.units import cm  # This is how many point there in a cm
import os
from reportlab.platypus import Table, TableStyle
from reportlab.lib import colors

# Setta la working directory al path dello script
abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)
c = canvas.Canvas("table.pdf", pagesize=landscape(A4), bottomup=1)
data = [['Header1', 'Header2', 'Header3'],
        ['row0-1', 'row0-2', 'row0-3'],
        ['row1-1', 'row1-2', 'row1-3'],
        ['row2-1', 'row2-2', 'row2-3'],
        ['row3-1', 'row3-2', 'row3-3'],
        ['row4-1', 'row4-2', 'row4-3'],
        ['row5-1', 'row5-2', 'row5-3'],
        ['row6-1', 'row6-2', 'row6-3'],
        ]
# print(data)
# data = list(reversed(data))
# print(data)

LIST_STYLE = TableStyle(
    [('LINEABOVE', (0, 0), (-1, 0), 2, colors.green),
     ('LINEABOVE', (0, 1), (-1, -1), 0.25, colors.black),
     ('LINEBELOW', (0, -1), (-1, -1), 2, colors.red),
     ('TEXTCOLOR', (0, -2), (-1, -2), colors.green),
     ('BACKGROUND', (1, 1), (-2, -2), colors.green),
     ('ALIGN', (0, 0), (-1, -1), 'RIGHT')]
)

t = Table(data)
t.setStyle(LIST_STYLE)
c.setTitle("Table")
t.wrapOn(c, 27*cm, 19*cm)
t.drawOn(c, 1*cm, 1*cm)
c.showPage()
c.save()
