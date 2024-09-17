import os

import numpy as np
import pandas as pd

# Setta la working directory al path dello script
abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)
# load a CSV file into a DataFrame
df = pd.read_csv("data.csv")
print(df.head())

# calculate the average value of a column
mean_value = df["Età"].mean()
print("Average value:", mean_value)

# add a new column to the DataFrame
df["new_column"] = df["Nome"] + df["Città"]

# group the data by the values in a column and calculate the sum
grouped = df.groupby("Città").sum()
print(grouped)

# write the DataFrame back to a CSV file
df.to_csv("file1.csv", index=False)
# write the DataFrame back to a CSV file
df.to_csv("file2.csv", index=False)
# write the DataFrame back to a CSV file
df.to_csv("file2.csv", index=False)

# write the DataFrame back to a CSV file
df.to_csv("printed_data.csv", index=False)
# write the DataFrame back to a CSV file
df.to_csv("printed_data.csv", index=False)

# write the DataFrame back to a CSV file
df.to_csv("dated_data.csv", index=False)
# write the DataFrame back to a CSV file
df.to_csv("dated_data.csv", index=False)
# write the DataFrame back to a CSV file
df.to_csv("dated_data.csv", index=False)
