from ftplib import FTP
from datetime import datetime
import os



strServer = "ftp.brt.it"
strUtente = "0040114"
strPwd = ""
path="//carlidisk/trasporti/Trasporto secondario/Vettori/BRT/Consuntivi/"

start = datetime.now()
ftp = FTP(strServer)
ftp.login(strUtente,strPwd)
ftp.cwd("OLD")
# Get All Files
files = ftp.nlst()
# files = ftp.mlsd()
# a=ftp.retrlines('LIST')
# a=ftp.dir()
# Print out the files
for file in files:
    size=ftp.size(file)
    print("Size of {} is {}".format(file,ftp.size(file)))
    # os.path.isfile(path+file)
    if size > 2000 and not(os.path.isfile(path+file)):
        ftp.retrbinary("RETR " + file ,open(path + file, 'wb').write)

ftp.close()



end = datetime.now()
diff = end - start
print('All files for ' + str(diff.seconds) + 's')
