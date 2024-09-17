from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.units import cm  # This is how many point there in a cm
import os
from reportlab.platypus import BaseDocTemplate, Table, TableStyle, SimpleDocTemplate, NextPageTemplate, PageTemplate, BaseDocTemplate
from reportlab.platypus.paragraph import Paragraph
from reportlab.platypus.flowables import PageBreak, Image, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.platypus.frames import Frame
from functools import partial
from reportlab.lib.enums import TA_CENTER


# Setta la working directory al path dello script
abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

header = ['Header1', 'Header2', 'Header3']

row0 = ['row0-1', 'row0-2', 'row0-3']
row1 = ['row1-1', 'row1-2', 'row1-3']
row2 = ['row2-1', 'row2-2', 'row2-3']
row3 = ['row3-1', 'row3-2', 'row3-3']
row4 = ['row4-1', 'row4-2', 'row4-3']
row5 = ['row5-1', 'row5-2', 'row5-3']
row6 = ['row6-1', 'row6-2', 'row6-3']

data_table = [header]
for _ in range(1, 20):
    data_table.extend((row0, row1, row2, row3, row4, row5, row6))
# print(data_table)
LIST_STYLES = TableStyle(
    [('LINEABOVE', (0, 0), (-1, 0), 2, colors.green),
     #     ('LINEABOVE', (0, 1), (-1, -1), 0.25, colors.black),
     ('LINEBELOW', (0, -1), (-1, -1), 2, colors.red),
     #  ('TEXTCOLOR', (0, -2), (-1, -2), colors.blueviolet),
     #      ('BACKGROUND', (1, 1), (-2, -2), colors.green),
     ('BACKGROUND', (0, 0), (-1, 0), colors.pink),
     ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
     ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
     ('BOX', (0, 0), (-1, -1), 2, colors.black),
     ('ROWBACKGROUNDS', (0, 1), (-1, -1), (colors.beige, colors.aquamarine))
     ]
)

styles = getSampleStyleSheet()
styles.add(ParagraphStyle(name='centered_wide', alignment=TA_CENTER,
                          leading=18, parent=styles['Heading1']))
t = Table(data_table, repeatRows=1)
t.setStyle(LIST_STYLES)
t.hAlign = 'LEFT'
t.vAlign = 'TOP'
story = [Spacer(cm, 5*cm)]
story.append(Paragraph("List of Batteries", styles['centered_wide']))
# story.append(Paragraph("Lanes", styles['Heading2']))
story.append(PageBreak())


story.append(t)
# print(story)

pdf = BaseDocTemplate('table_simple.pdf',
                      pagesize=landscape(A4),
                      title='ReportLab Training',
                      leftMargin=2.2 * cm,
                      rightMargin=2.2 * cm,
                      topMargin=1.5 * cm,
                      bottomMargin=2.5 * cm,
                      showBoundary=0)


frame = Frame(pdf.leftMargin, pdf.bottomMargin,
              pdf.width, pdf.height, showBoundary=0, id='normal')


def header_and_footer(canvas, doc):
    """
    Funzione per creare sulla canvas l'header ed il footer.
    A questo tipo di funzioni chiamate dall'argomento onPage vengono passati la canvas ed il documento
    """
    # print(canvas)
    # print(dir(canvas))
    # print(doc)
    # print(dir(doc))

    # Header
    canvas.saveState()
    content = Image('favicon.png', width=20, height=20)
    w, h = content.wrap(doc.width, doc.topMargin)
    content.drawOn(canvas, doc.leftMargin, doc.height +
                   doc.bottomMargin + doc.topMargin - h-cm/2)
    content = Paragraph("Managing batteries", styles['Normal'])
    w, h = content.wrap(doc.width, doc.topMargin)
    content.drawOn(canvas, doc.leftMargin+cm, doc.height +
                   doc.bottomMargin + doc.topMargin - h-cm/2)
    # Footer
    content = Paragraph("www.forte-family.it", styles['Normal'])
    w, h = content.wrap(doc.width, doc.bottomMargin)
    content.drawOn(canvas, doc.leftMargin, h+cm/2)

    title = doc.title
    fontsize = 12
    fontname = 'Helvetica'
    headerBottom = doc.bottomMargin+doc.height+doc.topMargin/2
    bottomLine = doc.bottomMargin+doc.height
    topLine = headerBottom + fontsize
    lineLength = doc.width+doc.leftMargin
    canvas.setFont(fontname, fontsize)
    # if doc.page % 2:
    #     # odd page: put the page number on the right and align right
    title += f"-{str(doc.page)}"
    canvas.drawRightString(lineLength, headerBottom, title)
    # else:
    #     # even page: put the page number on the left and align left
    # title = str(doc.page) + "-" + title
    # canvas.drawString(doc.leftMargin, headerBottom, title)
    # draw some lines to make it look cool
    canvas.setLineWidth(1)
    canvas.line(doc.leftMargin, bottomLine, lineLength, bottomLine)
    canvas.line(doc.leftMargin, topLine, lineLength, topLine)
    canvas.line(doc.leftMargin, bottomLine-doc.height,
                lineLength, bottomLine-doc.height)
    canvas.line(doc.leftMargin, bottomLine-doc.height-doc.bottomMargin/2-fontsize,
                lineLength, bottomLine-doc.height-doc.bottomMargin/2-fontsize)

    canvas.restoreState()


template = PageTemplate(id='page', frames=[frame], onPage=header_and_footer)

pdf.addPageTemplates([template])

pdf.build(story)

########### CODE SNIPPET ####################
# tableFrame = Frame(x1=pdf.leftMargin,
#                    y1=pdf.topMargin,
#                    width=pdf.width,
#                    height=pdf.height,
#                    showBoundary=1)
# more_header_content = Paragraph(
#     "Managing batteries", styles['Normal'])
# header_content = Image('favicon.png', width=20, height=20)
# footer_content = Paragraph(
#     "www.forte-family.it", styles['Normal'])
# def header(canvas, doc, content):
#     canvas.saveState()
#     w, h = content.wrap(doc.width, doc.topMargin)
#     content.drawOn(canvas, doc.leftMargin, doc.height +
#                    doc.bottomMargin + doc.topMargin - h-cm/2)
#     canvas.restoreState()


# def more_header(canvas, doc, content):
#     canvas.saveState()
#     w, h = content.wrap(doc.width, doc.topMargin)
#     content.drawOn(canvas, doc.leftMargin+cm, doc.height +
#                    doc.bottomMargin + doc.topMargin - h-cm/2)
#     canvas.restoreState()


# def footer(canvas, doc, content):
#     canvas.saveState()
#     w, h = content.wrap(doc.width, doc.bottomMargin)
#     content.drawOn(canvas, doc.leftMargin, h+cm/2)
#     canvas.restoreState()
# def header_and_footer(canvas, doc, header_content, footer_content, more_header_content):
#     header(canvas, doc, header_content)
#     more_header(canvas, doc, more_header_content)
#     footer(canvas, doc, footer_content)
# template = PageTemplate(id='test', frames=[frame], onPage=partial(
#     header_and_footer, header_content=header_content, footer_content=footer_content, more_header_content=more_header_content))
# lst.append(PageBreak())
# lst.append(Paragraph("""
#         Dopo le tabelle
#         """, styles['BodyText']))
# pdf.build([t])
# for item in list(styles.byAlias):
#     print(item)
# print()
# for item in list(styles.byName):
#     print(item)
# print(type(styles.byAlias))
