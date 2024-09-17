import sqlite3
conn = sqlite3.connect("data.db")
conn.row_factory = sqlite3.Row
c = conn.cursor()
item = [11, 'caffeina', 10]
riga = {"id": 12, "name": "kava", "price": 125}
c.execute("INSERT INTO coffe values (?,?,?)", item)
c.execute("INSERT INTO coffe values (:id,:name,:price)", riga)
conn.commit()


c.execute("select * from coffe where id = 12")
# row = c.fetchone()
# print(row.keys())
for row in c.fetchall():
    print(tuple(row))
    print(row['id'], row['name'], row['price'])
    print(f"(id = {row[0]} | nome = {row[1]} | kg = {row[2]})")
    print(f"(id = {row['id']} | nome = {row['name']} | kg = {row['price']})")


conn.close()
