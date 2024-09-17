from models import session, engine, Sp_Sped, Sp_Sped1
from sqlalchemy import and_, or_, select, desc
from sqlalchemy import func
import datetime
import pandas as pd
print("#### 1 ####")
with session:
    speds = session.query(Sp_Sped).where(
        Sp_Sped.NUM_SPED == '0600000').order_by(desc(Sp_Sped.DATA_SPED)).all()
    for sped in speds:
        print(
            f"In data '{sped.DATA_SPED.date()}' con numero '{sped.NUM_SPED}' è stata spedita la merce al cliente {sped.COD_CLIENTE}")

print("\n")
print("#### 2 ####")

with session:
    speds = session.query(Sp_Sped, Sp_Sped1).join(Sp_Sped1, (Sp_Sped.DATA_SPED == Sp_Sped1.DATA_SPED) & (Sp_Sped.NUM_SPED == Sp_Sped1.NUM_SPED)).where(
        Sp_Sped.NUM_SPED == '0600000').order_by(desc(Sp_Sped.DATA_SPED)).all()
    # print(speds)
    # for sped in speds:
    #     print(sped)
    for sped, sped1 in speds:
        print(
            f"In data '{sped.DATA_SPED.date()}' con numero '{sped.NUM_SPED}' è stata spedita la merce al cliente {sped.COD_CLIENTE}. Flag Complessa: {sped1.FLAG_COMPLESSA}")

stmt = select(Sp_Sped).where(
    Sp_Sped.NUM_SPED == '0600000').order_by(desc(Sp_Sped.DATA_SPED))
print(stmt)
conn = engine.connect(close_with_result=True)
df = pd.read_sql(stmt, conn)
print(df)

speds = session.scalars(select(Sp_Sped).where(
    Sp_Sped.NUM_SPED == '0600000').order_by(desc(Sp_Sped.DATA_SPED)))
records = []
for item in speds:
    print("\n")
    print(item.DATA_SPED, item.NUM_SPED)
    row = [getattr(item, key)
           for key in Sp_Sped.__table__.columns.keys()]
    print(row)
    records.append(row)

intestazioni = list(Sp_Sped.__table__.columns.keys())
df = pd.DataFrame.from_records(records, columns=intestazioni)
print(df)
