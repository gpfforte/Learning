from ftplib import FTP
import os
from datetime import datetime
now = datetime.now()
date_time = now.strftime("-%Y-%m-%d-%H%M%S")

ftp = FTP('ftp.us.debian.org')
ftp.getwelcome()
ftp.login()
ftp.cwd('debian')
# ftp.cwd('doc')
# ftp.retrlines('LIST')
ftp.mlsd()
ftp.nlst()
ftp.dir()
with open('extrafiles', 'wb') as fp:
    ftp.retrbinary('RETR extrafiles', fp.write)
os.rename(fp.name, "Extra"+date_time)

ftp.quit()
