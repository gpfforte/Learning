from datetime import datetime
import pytz
from sqlalchemy import create_engine, text

engine = create_engine("sqlite+pysqlite:///:memory:", echo=False, future=True)
tz = pytz.timezone('Europe/Rome')
utc_now = datetime.utcnow()
local_time_current = pytz.utc.localize(
    utc_now, is_dst=None).astimezone(tz)
local_time_current_readable= local_time_current.strftime('%Y-%m-%d %H:%M:%S')
# print (local_time_current)
# print(local_time_current_readable)

# with engine.connect() as conn:
#      result = conn.execute(text("select 'hello world'"))
#      print(result.all())
# "commit as you go"
# with engine.connect() as conn:
#      conn.execute(text("CREATE TABLE some_table (x int, y int)"))
#      conn.execute(
#          text("INSERT INTO some_table (x, y) VALUES (:x, :y)"),
#          [{"x": 1, "y": 1}, {"x": 2, "y": 4}]
#      )
#      conn.commit()

# "begin once"
with engine.begin() as conn:
    conn.execute(text("CREATE TABLE some_table (x int, y int)"))
    conn.execute(
         text("INSERT INTO some_table (x, y) VALUES (:x, :y)"),
         [{"x": 1, "y": 1}, {"x": 2, "y": 4}]
     )
    conn.execute(
         text("INSERT INTO some_table (x, y) VALUES (:x, :y)"),
         [{"x": 6, "y": 8}, {"x": 9, "y": 10}]
     )

with engine.connect() as conn:
    result = conn.execute(text("SELECT x, y FROM some_table"))
    
    for row in result:
         print(f"x: {row.x}  y: {row.y}")
    