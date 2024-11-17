zone_consegne_presso_emporio_tupla = (
    "199",
    "901",
    "902",
    "903",
    "904",
    "905",
    "906",
    "907",
    "908",
    "909",
    "910",
    "911",
)
depositi_escludere_in_vpc_tupla = (
    "04",
    "36",
    "3D",
    "3G",
    # "58",
    "83",
    "3B",
    "5D",
    "5F",
    "5X",
    "5P",
    "5R",
    "EC",
    "EP",
)
zone_brt_tupla = (
    "999",
    "435",
    "480",
    "703",
    "403",
    "211",
    "209",
)  # 703 vuota al 18/09/2023
zone_isole_vpc_tupla = ("436", "437")
depositi_chiusi_tls = "XX"
depositi_chiusi_dem = "XX"
# Di seguito i giorni relativi agli ordini TLS inseriti fino a quel giorno su quelle zone che devono essere garantiti, la data tiene conto del fatto che
# gli ordini TLS saranno inseriti il giorno dopo rispetto alla presa dell'ordine
zone_da_recuperare_ordini_tls = {
    "20231213": ("299", "321", "718", "187", "286")}
depositi_da_recuperare_ordini_tls = {"20231213": ("24", "21")}
consegne_giorno_traspo = {
    "01": 45,
    # "03": 55,
    "06": 55,
    "07": 250,
    "09": 335,
    "10": 700,  # da cambiare, attendere da LER
    # "13": 280,
    "14": 740,  # Cambiato ad Assago il 16/09/2024 # da cambiare, attendere da LER
    "21": 370,  # riescono a garantircele anche quest'anno - riunione 07/10/2024
    "24": 100,  # 45 Tomasi e 60-65 Brazzarola
    # "26": 70, # VOLPATO
    "27": 70,
    "31": 750,
    "32": 130,
    "34": 65,
    "35": 70,  # da cambiare, attendere da LER
    "38": 80,
    "40": 230,  # A Natale 2022 era passato a 160 da 240. 300 a Roma il 29/03/2023, ma si sono rimangiati la parola il 01/12/2023, 230 mail 17/06/2024 da Gattuso
    "41": 200,
    "42": 140,
    # "56": 750,  # 750
    "57": 900,  # Suleri ne ha promesse 1000
    "58": 40,
    # "59": 35,
    "63": 50,
    # "64": 80,
    "65": 35,  # Mail Galimberti 02/12/2023
    # "66": 50,
    "67": 170,  # In occasione ultima visita a inizio Luglio 2024
    # "69": 80,
    "6O": 104,
    # "79": 150, # ULI
    # "89": 40, # LOGTRAS
    "8T": 100,
    "8V": 50,
}
OPID_CALL_CENTER = (
    "MVA",  # Marchisio Valentina
    "AIF",  # Aicardi Federica
    "AM ",  # Arzani Manuela
    "BA ",  # Bellone Annamaria
    "BIS",  # Bianchi Simona
    "NUN",  # Nuvoli Nicla
    "FAB",  # Fama' Beatrice
    "DEB",  # Dellavalle Barbara
    "GID",  # Giudice Daniela
    "FM ",  # Ferrero Michela
    "ADA",  # Accatino Daniela
    "MGS",  # Magliano Serenella
    "MSI",  # Marino Simona
    "MSE",  # Martino Serena
    "MSA",  # Mela Sandra
    "PH ",  # Pirani Helga
    "LOF",  # Longaretti Francesca
    "ROD",  # Roncallo Daniela
    "MIE",  # Miano Serena
    "SAA",  # Sasso Annalisa
    "RUV",  # Ruella Valentina
    "TCA",  # Tealdi Caterina
    "BMT",  # Ballini Martina
)

STATI_SF = {
    "01": "BOZZA",
    "02": "BLOCCATO",
    "03": "SPEDIBILE",
    "04": "EVASO",
    "05": "05",
    "06": "CONSEGNATO",
    "08": "RESO",
    "09": "ANNULLATO",
}
# \\carlidisk\trasporti\Trasporto secondario\Trasportatori\Fidejussioni\FIDEJUSSIONI.xlsx
FIDE = {
    '01': [15000, True],
    '06': [15000, True],
    '07': [75000, True],
    '09': [40000, False],
    '10': [120000, True],
    '14': [150000, True],
    '21': [80000, True],
    '24': [30000, True],
    '27': [30000, True],
    '31': [150000, True],
    '32': [45000, True],
    '34': [15000, True],
    '35': [30000, True],
    '38': [30000, True],
    '40': [50000, True],
    '41': [50000, True],
    '42': [30000, True],
    '57': [100000, True],
    '6O': [40000, True],
    '65': [15000, True],
    '67': [50000, True],
    '8T': [20000, True],
}
