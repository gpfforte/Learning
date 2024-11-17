import datetime as dt
import os
from logging import DEBUG

from supabase import Client, ClientOptions, create_client

from servizio import log_setup

filename, _ = os.path.splitext(os.path.basename(__file__))
logger = log_setup.logging_setup(
    nomefile=filename, levelfile=DEBUG, name=__name__)

PROVA = bool(os.environ.get("AMBIENTE_DI_PROVA") == "SI")

url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(url, key,
                                 options=ClientOptions(
                                     postgrest_client_timeout=10,
                                     storage_client_timeout=10
                                 ))

# response = supabase.table('fuel_history').select("*").execute()
# print(response)

now = dt.datetime.now()
date_time = now.strftime("%Y-%m-%d-%H%M%S")
date_now = now.strftime("%Y-%m-%d")


def main():
    # dict_fuels = {}
    # price, count = supabase.table('fuel_history').select(
    #     'prezzo_lordo, anno, codice_mese').gte('anno', 2022).execute()
    # for item in price[1]:
    #     prezzo = round(item['prezzo_lordo'] / 1000, 3)
    #     dict_fuels[f"{item['anno']}-{item['codice_mese']:02}"] = prezzo
    # print(price[1])
    # data, count = supabase.table('conv_rif_carli_rif_brt')\
    #     .insert({"riferimento_carli": 30000000000,
    #             "riferimento_brt": 4020000000,
    #              "created_at": date_now
    #              })\
    #     .execute()
    spedizioni = supabase.table(
        "spedizioni_brt_contrassegno").select("*").gte("riferimento_carli", 20231803207).execute()
    spedizioni = supabase.table(
        "conv_rif_carli_rif_brt").select("*").gte("riferimento_carli", 20240000000).execute()
    print("spedizioni.data:", spedizioni.data)
    # print("spedizioni.data[0]:", spedizioni.data[0])
    # print("spedizioni.count:", spedizioni.count)
    # print(dir(spedizioni))
    print(type(spedizioni.data[0]))
    # df = pd.DataFrame.from_dict(spedizioni[1]).rename(
    #     columns={"riferimento_carli": "Riferimento Carli"})
    # print(count)


# stmt = select(Fuel).where(Fuel.anno.__ge__(anno_inizio - 1))
# for price in session_sb.scalars(stmt):
#     prezzo = round(price.prezzo_lordo / 1000, 3)
#     dict_fuels[f"{price.anno}-{price.codice_mese:02}"] = prezzo

if __name__ == "__main__":
    try:
        main()
        # print(DB_POSTGRESQL_PORT)
    except Exception as e:
        if PROVA:
            logger.info(e, exc_info=True)
        else:
            logger.critical(e, exc_info=True)
