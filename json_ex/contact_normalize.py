import pandas as pd
import json
from pathlib import Path
# Load the JSON data
with open(f'{Path(__file__).parent}/contact_reduced.json', 'r') as file:
    data = json.load(file)

# Flatten the JSON data into a DataFrame
df = pd.json_normalize(data["results"])

# Print the DataFrame
print(df)