import smtplib
from email.message import EmailMessage
from email.policy import SMTP
import os
import mimetypes
import email_body
from string import Template
import email_body

# Setta la working directory al path dello script
abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

EMAIL_HOST_USER = os.environ.get("EMAIL_HOST_USER")
EMAIL_HOST_SERVER = 'localhost'
# EMAIL_HOST_SERVER = 'mail.oliocarli.it'
EMAIL_HOST_PASSWORD = os.environ.get("EMAIL_HOST_PASSWORD")

msg = EmailMessage()      # create a message


body = """Prova Invio Email"""
# body.substitute(link="GGPPFF")
# setup the parameters of the message
msg['From'] = EMAIL_HOST_USER
msg['To'] = "gpf_forte@hotmail.com"
msg["Subject"] = "Prova"
msg.set_content(body, subtype='html')
msg.preamble = 'You will not see this in a MIME-aware mail reader.\n'

#filename="Situazione Consegne_2021-01-24-220249.csv"
filename = ""
# filename = "Images/1.jpg"

ctype, encoding = mimetypes.guess_type(filename)
if ctype is None or encoding is not None:
    # No guess could be made, or the file is encoded (compressed), so
    # use a generic bag-of-bits type.
    ctype = 'application/octet-stream'
maintype, subtype = ctype.split('/', 1)

if filename:
    with open(filename, 'rb') as fp:
        msg.add_attachment(fp.read(),
                           maintype=maintype,
                           subtype=subtype,
                           filename=filename)

print(msg.items())


# set up the SMTP server
s = smtplib.SMTP(host=EMAIL_HOST_SERVER, port=1025)
# s.starttls()
# s.login(EMAIL_HOST_USER, EMAIL_HOST_PASSWORD)

# send the message via the server set up earlier.
s.send_message(msg)
s.quit()
del msg
