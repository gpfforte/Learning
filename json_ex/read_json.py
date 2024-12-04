import json
from pathlib import Path
import pandas as pd
# Open and read the JSON file
print("Read Json file")
with open(f'{Path(__file__).parent}/sample.json', 'r') as file:
    data = json.load(file)

# Print the data
# print(data)
# print(type(data))
for item in data["emp_details"]:
   print(item["emp_name"]) 
print("")

print("Read Json with pandas")
df=pd.read_json(f'{Path(__file__).parent}/sample.json')

# print(df)
# print(df.iloc[0])

for row in df.iterrows():
    # print(row)
    # print(type(row))
    # print(row[1])
    # print(len(row[1]))
    # print(type(row[1]))
    print(row[1].iloc[0]['emp_name'])
