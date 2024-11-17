import mimetypes
import os
import smtplib
import time
from datetime import datetime as dt
from email.message import EmailMessage

import holidays
import zeep

from servizio.costanti import OPID_CALL_CENTER
from servizio.supabase_db_2024 import supabase

now = dt.now()
date_time = now.strftime("%Y-%m-%d-%H%M%S")
date_now = now.strftime("%Y-%m-%d")
cliente_id = []
cliente_id.append(os.environ.get("BRT_FTP_USER"))
cliente_id.append(os.environ.get("BRT_FTP_2023_USER"))
# Questa prima parte di ricerca trova la spedizione con il riferimento Carli (quello numerico composto da anno+numero spedizione paddato a 7)
# Il servizio non richiede autenticazione
# wsdl_ric = "http://wsr.brt.it:10041/web/GetIdSpedizioneByRMNService/GetIdSpedizioneByRMN?wsdl"
wsdl_ric = (
    "https://wsr.brt.it:10052/web/GetIdSpedizioneByRMNService/GetIdSpedizioneByRMN?wsdl"
)
client_ric = zeep.Client(wsdl=wsdl_ric)

# wsdl_brt_id = "http://wsr.brt.it:10041/web/BRT_TrackingByBRTshipmentIDService/BRT_TrackingByBRTshipmentID?wsdl"
wsdl_brt_id = "https://wsr.brt.it:10052/web/BRT_TrackingByBRTshipmentIDService/BRT_TrackingByBRTshipmentID?wsdl"
client_brt_id = zeep.Client(wsdl=wsdl_brt_id)


def color_backgound_2(val, **kwargs):
    color = ""
    minimo = kwargs.get("minimo", 0)
    massimo = kwargs.get("massimo", 1)
    intervallo = (massimo - minimo) / 4
    val1 = minimo + intervallo
    val2 = val1 + intervallo
    val3 = val2 + intervallo
    # print(val, minimo, massimo, val1, val2, val3)
    if val < val1:
        color = "green"
    if val >= val1 and val < val2:
        color = "yellow"
    if val >= val2 and val < val3:
        color = "orange"
    if val >= val3:
        color = "red"
    return f"background-color: {color}" if color else ""


def color_backgound_1(val, **kwargs):
    color = ""
    minimo = kwargs.get("minimo", 0)
    massimo = kwargs.get("massimo", 1)
    intervallo = (massimo - minimo) / 4
    val1 = minimo + intervallo
    val2 = val1 + intervallo
    val3 = val2 + intervallo
    if val < val1:
        color = "red"
    if val >= val1 and val < val2:
        color = "orange"
    if val >= val2 and val < val3:
        color = "yellow"
    if val >= val3:
        color = "green"
    return f"background-color: {color}" if color else ""


def identifica_reparto(x):
    """
    In base alla tupla TIPO_IMMISSIONE e OPID determina il reparto/call center corrispondente
    """
    if x[0] == "I":
        return "INTERNET"
    if x[0] == "L":
        return "TLS"
    if x[0] == "N":
        return "NEGOZIO"
    if x[0] == "R":
        return "LETTORE"
    if x[0] == "T" and x[1][0] == "Y":
        return "8MILA"
    if x[0] == "T" and x[1][0] == "C":
        return "COMDATA"
    if x[0] == "T" and x[1][0] == "W":
        return "S3C"
    if x[0] == "T" and x[1] in OPID_CALL_CENTER:
        return "CALL CENTER INTERNO"
    return "ALTRO"


def invio_email(logger, filename=None, destinatari=None, soggetto=None, contenuto=None, script=None):
    if destinatari is None:
        logger.critical(f"Email inviata a {destinatari}")
        raise ValueError(
            "In Invio Email non sono stati specificati destinatari")
    if filename is None:
        filename = ""
    EMAIL_HOST_USER = os.environ.get("EMAIL_HOST_USER")
    EMAIL_HOST_SERVER = os.environ.get("EMAIL_HOST_SERVER")
    EMAIL_HOST_PASSWORD = os.environ.get("EMAIL_HOST_PASSWORD")

    msg = EmailMessage()  # create a message
    # setup the parameters of the message
    msg["From"] = EMAIL_HOST_USER
    msg["To"] = destinatari
    msg["Subject"] = soggetto
    if script:
        contenuto = f"""
                {contenuto}
                        <br>
                        <br>
                <hr>
                        <p>Script: {script}</p>
                """
    msg.set_content(contenuto, subtype="html")
    msg.preamble = "You will not see this in a MIME-aware mail reader.\n"
    if type(filename) is list:
        ctype, encoding = mimetypes.guess_type(filename[0])
    else:
        ctype, encoding = mimetypes.guess_type(filename)

    if ctype is None or encoding is not None:
        # No guess could be made, or the file is encoded (compressed), so
        # use a generic bag-of-bits type.
        ctype = "application/octet-stream"
    maintype, subtype = ctype.split("/", 1)
    if filename:
        if type(filename) is list:
            for file in filename:
                with open(file, "rb") as fp:
                    msg.add_attachment(
                        fp.read(), maintype=maintype, subtype=subtype, filename=file
                    )
        else:
            with open(filename, "rb") as fp:
                msg.add_attachment(
                    fp.read(), maintype=maintype, subtype=subtype, filename=filename
                )

    # set up the SMTP server
    s = smtplib.SMTP(host=EMAIL_HOST_SERVER, port=587)
    s.starttls()
    s.login(EMAIL_HOST_USER, EMAIL_HOST_PASSWORD)

    # send the message via the server set up earlier.
    s.send_message(msg)
    logger.info(f"Email con oggetto {soggetto} inviata a {destinatari}")
    s.quit()
    del msg


def rgb_to_hex(rgb):
    # Prende in input una tupla di valori rgb e restituisce il corripondente colore in esadecimale
    return "#%02x%02x%02x" % rgb


def add_working_days(x):
    """
    Occhio che i sabati in questa funzione sono considerati lavorativi
    """
    # Prende in input una lista e in base ai sabati, domeniche e alle vacanze calcola da una data di partenza una data di arrivo
    # sommando i giorni lavorativi
    # X[0]=data di partenza, X[1] giorni da aggiungere
    # La data che prende in ipunt deve arrivare da una conversione pd.to_datetime che
    # ritorna un pandas._libs.tslibs.timestamps.Timestamp
    today = dt.datetime.now()
    list_hol = [
        date
        for date, name in sorted(
            holidays.IT(years=[today.year, today.year + 1]).items()
        )
    ]
    days_elapsed = 0
    while days_elapsed < x[1]:
        test_date = x[0] + dt.timedelta(days=1)
        # print(type(test_date))
        x[0] = test_date

        if test_date.weekday() > 5 or test_date.to_pydatetime().date() in list_hol:
            # if a sunday or holiday skip
            continue
        else:
            # if a workday, count as a day
            days_elapsed += 1

    return x[0]


def export_to_csv(logger, df, nomefile):
    logger.debug("export_to_csv iniziata")
    nome_completo = f"{nomefile}_{date_time}.csv"
    df.to_csv(nome_completo, index=False, sep=";",
              encoding="UTF-8", decimal=",")
    logger.info(fr"{os.getcwd()}\{nome_completo}")
    logger.debug("export_to_csv terminata")
    return nome_completo


def export_to_xlsx(logger, df, nomefile):
    logger.debug("export_to_xlsx iniziata")
    nome_completo = f"{nomefile}_{date_time}.xlsx"
    df.to_excel(nome_completo, index=False, sheet_name="Report")
    logger.info(fr"{os.getcwd()}\{nome_completo}")
    logger.debug("export_to_xlsx terminata")
    return nome_completo


def cerca_brt_code(riferimento_numerico_carli):
    """Funzione per cercare nel db locale (in realtà su Supabase) se esiste già il BRT Code per il riferimento in
    input
    """
    riferimento, count = supabase.table('conv_rif_carli_rif_brt').select(
        'riferimento_brt')\
        .eq('riferimento_carli', riferimento_numerico_carli)\
        .execute()

    # with session_sb:
    #     riferimento = (
    #         session_sb.query(MapRifCarliBrt)
    #         .where(MapRifCarliBrt.riferimento_carli == riferimento_numerico_carli)
    #         .one_or_none()
    #     )
    if riferimento[1]:
        return riferimento[1][0]["riferimento_brt"]
    return 0


def ricerca_spedizione_brt_ultimo(args, logger, ultimo=True):
    """
    Funzione per trovare l'ultimo esito di una spedizione BRT. In input riceve una tupla con ("RIFERIMENTO_MITTENTE_NUMERICO", "DATA_SPED", "ANNO") e restituisce una tupla
    ("DESCRIZIONE","DATA", "ORA", "FILIALE","ID_SPEDIZIONE_BRT") dell'ultimo esito (se presente).
    Cerca nel db su SUPABASE con il riferimento mittente numerico, l' di spedizione BRT. Se non lo trova interroga BRT con il riferimento mittente numerico, se trova l'ID
    segnala come descrizione esito "NON PRESENTE". Se invece con l'ID BRT non trova esiti segnala "NON TROVATO" (caso che non succede praticamente mai).
    A seconda del parametro "ultimo" ritorna l'ultimo esito o la lista di tutti gli esiti.
    """
    time.sleep(1)
    logger.info("Inizio Spedizione")
    risultato = {}
    riferimento_numerico_carli = str(args[0])
    data_sped = args[1].strftime("%Y-%m-%d")
    anno = args[2]
    riferimento = cerca_brt_code(riferimento_numerico_carli)

    if not riferimento:
        now = dt.now()
        seconds = dt.timestamp(now)
        logger.info(
            "Riferimento Numerico Carli = "
            + str(riferimento_numerico_carli)
            + "|"
            + data_sped
            + " non trovato nel DB Locale"
        )
        # Sotto serve per non fare più di 3600 chiamate all'ora
        # if (seconds - seconds_prev) <= 1:
        #     time.sleep(1)

        # Il parametro da passare è costituito da un dizionario con i valori da passare ed il codice cliente Carli che è fisso
        parametro_ric = {
            "RIFERIMENTO_MITTENTE_NUMERICO": riferimento_numerico_carli,
            "CLIENTE_ID": cliente_id[1],
        }
        # Ricavo il numero di spedizione BRT che serve per fare l'interrogazione completa, lo ritrovo come valore della chiave SPEDIZIONE_ID

        risultato = client_ric.service.getidspedizionebyrmn(parametro_ric)
        logger.info(f'risultato[ESITO]: {risultato["ESITO"]}')

        if risultato["ESITO"] < 0:
            logger.info(f'Dentro if risultato[ESITO]: {risultato["ESITO"]}')
            parametro_ric = {
                "RIFERIMENTO_MITTENTE_NUMERICO": riferimento_numerico_carli,
                "CLIENTE_ID": cliente_id[0],
            }
            risultato = client_ric.service.getidspedizionebyrmn(parametro_ric)

        if risultato["ESITO"] >= 0:
            id_spedizione_brt = str(risultato["SPEDIZIONE_ID"])
            data, count = supabase.table('conv_rif_carli_rif_brt')\
                .insert({"riferimento_carli": riferimento_numerico_carli,
                        "riferimento_brt": id_spedizione_brt,
                         "created_at": date_now
                         })\
                .execute()
            # with session_sb:
            #     riferimento = MapRifCarliBrt(
            #         riferimento_brt=id_spedizione_brt,
            #         riferimento_carli=riferimento_numerico_carli,
            #         # created_at=today_date,
            #     )
            #     session_sb.add(riferimento)
            #     session_sb.commit()

            logger.info(
                "Riferimento Numerico Carli = "
                + str(riferimento_numerico_carli)
                + "|"
                + data_sped
                + " trovato in BRT con numero BRT = "
                + str(id_spedizione_brt)
                + " inserito in DB Locale"
            )
        else:
            logger.info(
                "Riferimento Numerico Carli = "
                + str(riferimento_numerico_carli)
                + "|"
                + data_sped
                + " non trovato in BRT con riferimento cliente"
            )
    else:
        # impostare esito = 1 serve solo per farlo entrare nella if corretta successiva
        risultato["ESITO"] = 1
        risultato["SPEDIZIONE_ID"] = riferimento
        logger.info(
            "Riferimento Numerico Carli = "
            + str(riferimento_numerico_carli)
            + "|"
            + data_sped
            + " trovato nel DB Locale con numero BRT = "
            + str(risultato["SPEDIZIONE_ID"])
        )
    if risultato["ESITO"] >= 0 or risultato["SPEDIZIONE_ID"]:
        id_spedizione_brt = risultato["SPEDIZIONE_ID"]
        now = dt.now()
        seconds = dt.timestamp(now)
        logger.info(
            "Riferimento Numerico Carli = "
            + str(riferimento_numerico_carli)
            + "|"
            + data_sped
            + " "
            + "Ricerca Esiti Spedizione BRT = "
            + str(id_spedizione_brt)
        )
        # Sotto serve per non fare più di 3600 chiamate all'ora
        # if (seconds - seconds_prev) <= 1:
        #     time.sleep(1)
        seconds_prev = seconds

        parametro = {
            "LINGUA_ISO639_ALPHA2": "it",
            "SPEDIZIONE_ANNO": anno,
            "SPEDIZIONE_BRT_ID": id_spedizione_brt,
        }

        risultato = client_brt_id.service.brt_trackingbybrtshipmentid(
            parametro)
        # logger.info(risultato)
        numero_eventi = risultato["CONTATORE_EVENTI"]
        logger.info(f"numero_eventi: {numero_eventi}")
        if risultato["ESITO"] >= 0:
            lista_eventi = risultato["LISTA_EVENTI"][0:numero_eventi]
            # logger.info(lista_eventi)
            logger.info(
                "Riferimento Numerico Carli = "
                + str(riferimento_numerico_carli)
                + "|"
                + data_sped
                + " "
                + "Ricerca Esiti Spedizione BRT = "
                + str(id_spedizione_brt)
                + " Esiti Trovati"
            )
            # ritorna l'ultimo esito
            if ultimo:
                return (
                    lista_eventi[0]["EVENTO"]["DESCRIZIONE"],
                    lista_eventi[0]["EVENTO"]["DATA"],
                    lista_eventi[0]["EVENTO"]["ORA"],
                    lista_eventi[0]["EVENTO"]["FILIALE"],
                    "00" + str(id_spedizione_brt),
                )
            else:
                listone_eventi = []
                for evento in lista_eventi:
                    listone_eventi.append(
                        (
                            evento["EVENTO"]["DESCRIZIONE"],
                            evento["EVENTO"]["DATA"],
                            evento["EVENTO"]["ORA"],
                            evento["EVENTO"]["FILIALE"],
                        )
                    )
                return listone_eventi, "00" + str(id_spedizione_brt)
        else:
            logger.info("risultato['ESITO']: " + str(risultato["ESITO"]))
            logger.info(
                "Riferimento Numerico Carli = "
                + str(riferimento_numerico_carli)
                + "|"
                + data_sped
                + " "
                + "Ricerca Esiti Spedizione BRT = "
                + str(id_spedizione_brt)
                + " Esiti non Trovati con id_spedizione_BRT"
            )
            return "NON TROVATO", "", "", "", "00" + str(id_spedizione_brt)
    else:
        return "NON PRESENTE", "", "", "", ""


# def add_working_days(x):
#     # X[0]=data di partenza, X[1] giorni da aggiungere

#     global list_hol

#     days_elapsed = 0
#     while days_elapsed < x[1]:
#         # print(x[0].to_pydatetime().date())
#         # if x[0].to_pydatetime().date() in list_hol:
#         #     print("Entrato")
#         #     continue
#         test_date = x[0]+dt.timedelta(days=1)

#         # print(type(test_date.to_pydatetime()))
#         #  print(test_date)
#         x[0] = test_date
#         # print(test_date.to_pydatetime() in list_hol)
#         if test_date.weekday() > 5 or test_date.to_pydatetime().date() in list_hol:
#             # if a sunday or holiday skip
#             continue
#         else:
#             # if a workday, count as a day
#             days_elapsed += 1

#     return x[0]
