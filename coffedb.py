import sqlite3
conn=sqlite3.connect("data.db")
c=conn.cursor()
# item=[2,"arabica",180]
# c.execute("INSERT INTO coffe values (?,?,?)",item)

nome=["java"]

c.execute("select * from coffe where id = 1")
for row in c.fetchall():
	print ("(id = {} | nome = {} | kg = {})".format(row[0],row[1],row[2]))

conn.commit()
conn.close()
