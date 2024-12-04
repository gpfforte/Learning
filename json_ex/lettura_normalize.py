import pandas as pd
import json

from pathlib import Path
# Caricamento del file JSON
with open(f'{Path(__file__).parent}/data.json', 'r') as f:
    data = json.load(f)

# Struttura JSON semplificata (esempio):
# {
#     "dati": [
#         {
#             "chiave1": [
#                 {
#                     "chiave2": [
#                         {"valore1": 10, "valore2": 20},
#                         {"valore1": 15, "valore2": 25}
#                     ]
#                 }
#             ]
#         }
#     ]
# }

# Appiattimento e creazione del DataFrame
df = pd.json_normalize(data, record_path=['dati', 'chiave1', 'chiave2'], meta=['dati'])

# Applicazione di una formula (esempio: raddoppio di valore1)
df['valore1_doppio'] = df['valore1'] * 2

print(df)