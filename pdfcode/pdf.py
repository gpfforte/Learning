from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm  # This is how many point there in a cm
import os
# Setta la working directory al path dello script
abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

c = canvas.Canvas("hello.pdf", pagesize=A4)

print(cm)
width, height = A4  # in points
print(A4)
c.drawString(cm/2, cm/2, "Hello Pdf")
# move the origin up and to the left
c.translate(cm, cm)
# define a large font
c.setFont("Helvetica", 10)
# choose some colors
c.setStrokeColorRGB(0, 0, 0)
c.setFillColorRGB(1, 0, 1)
# draw a rectangle
c.rect(0, 0, 6*cm, 9*cm, fill=1)
# make text go straight up
c.rotate(90)
# change color
c.setFillColorRGB(0, 0, 0.77)
# say hello (note after rotate the y coord needs to be negative!)
c.drawString(1*cm, -1*cm, "Hello World")

c.showPage()
c.save()
