import zeep
cliente_id = "0040114"
##wsdl = 'http://www.soapclient.com/xml/soapresponder.wsdl'
##client = zeep.Client(wsdl=wsdl)
##print(client.service.Method1('Zeep', 'is cool'))

##


def ricerca_spedizione_brt(riferimento_numerico_carli):
    

    # Questa prima parte di ricerca trova la spedizione con il riferimento Carli (quello numerico composto da anno+numero spedizione paddato a 7)
    # Il servizio non richiede autenticazione
    wsdl_ric = "http://wsr.brt.it:10041/web/GetIdSpedizioneByRMNService/GetIdSpedizioneByRMN?wsdl"
    client_ric = zeep.Client(wsdl=wsdl_ric)

    # Il parametro da passare è costituito da un dizionario con i valori da passare ed il codice cliente Carli che è fisso
    parametro_ric={"RIFERIMENTO_MITTENTE_NUMERICO":riferimento_numerico_carli, "CLIENTE_ID":cliente_id}
    # Ricavo il numero di spedizione BRT che serve per fare l'interrogazione completa, lo ritrovo come valore della chiave SPEDIZIONE_ID
    id_spedizione_brt=client_ric.service.getidspedizionebyrmn(parametro_ric)["SPEDIZIONE_ID"]

    # print(client_ric.service.getidspedizionebyrmn(parametro_ric))

    wsdl = "http://wsr.brt.it:10041/web/BRT_TrackingByBRTshipmentIDService/BRT_TrackingByBRTshipmentID?wsdl"
    client = zeep.Client(wsdl=wsdl)
    parametro={"LINGUA_ISO639_ALPHA2":"", "SPEDIZIONE_ANNO":0,"SPEDIZIONE_BRT_ID":id_spedizione_brt}
    ## print(client.service.brt_trackingbybrtshipmentid(parametro)["BOLLA"]["RIFERIMENTI"])
    #print(client.service.brt_trackingbybrtshipmentid(parametro))
    # print(client.service.brt_trackingbybrtshipmentid(parametro)["CONTATORE_EVENTI"])
    lista_eventi=client.service.brt_trackingbybrtshipmentid(parametro)["LISTA_EVENTI"]
    for i in lista_eventi:
        pass
        # print(i)
    return (lista_eventi[0]['EVENTO'])

riferimento_numerico_carli=20210028255
ultimo_evento=ricerca_spedizione_brt(riferimento_numerico_carli)
print(ultimo_evento)
print("La spedizione riferimento Carli {} ha come ultimo evento {} il {} alle {}".format(riferimento_numerico_carli, ultimo_evento['DESCRIZIONE'], ultimo_evento['DATA'], ultimo_evento['ORA']))
