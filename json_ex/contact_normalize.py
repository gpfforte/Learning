import json
from pathlib import Path

import pandas as pd

# Load the JSON data
with open(f'{Path(__file__).parent}/contact.json', 'r') as file:
    data = json.load(file)

# # Flatten the JSON data into a DataFrame
# # df = pd.json_normalize(data["results"])

df = pd.json_normalize(data["results"], record_path=[
                       'data', 'metrics'], meta=['group'])

# data_list = []
# for result in data["results"]:
#     queue_id = result["group"]["queueId"]
#     media_type = result["group"]["mediaType"]
#     for data_point in result["data"]:
#         interval = data_point["interval"]
#         for metric in data_point["metrics"]:
#             metric_name = metric["metric"]
#             metric_value = metric["stats"]["count"] if metric_name == "nOffered" else metric["stats"]["ratio"]
#             data_list.append({
#                 "queueId": queue_id,
#                 "mediaType": media_type,
#                 "interval": interval,
#                 "metric": metric_name,
#                 "value": metric_value
#             })

# Create the Pandas DataFrame
# df = pd.DataFrame(data_list)


def extract_values(dictionary):
    queue = dictionary['queueId']
    mediatype = dictionary['mediaType']
    return queue, mediatype


df[["QUEUE", "MEDIATYPE"]] = df['group'].apply(
    lambda x: pd.Series(extract_values(x)))
# df[["QUEUE"], ["MEDIATYPE"]] = df["group"].values.get("queueId")

# Print the DataFrame
print(df)
