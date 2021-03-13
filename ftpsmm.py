from ftplib import FTP
from datetime import datetime

strServer = "192.168.155.103"
strUtente = "Carli201201"
strPwd = "29carli47899"

start = datetime.now()
ftp = FTP(strServer)
ftp.login(strUtente,strPwd)
ftp.cwd("Accisa")
# Get All Files
files = ftp.nlst()
a=ftp.retrlines('LIST')
# Print out the files
for file in files:
	print("Size of {} is {}".format(file,ftp.size(file)))
	#ftp.retrbinary("RETR " + file ,open("download/to/your/directory/" + file, 'wb').write)

ftp.close()

end = datetime.now()
diff = end - start
print('All files for ' + str(diff.seconds) + 's')
