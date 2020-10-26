import pandas as pd
import numpy as np

# PREPARING THE DATA
data_labels = [
    "timestamp", 
    "gender", 
    "hedge_first",
    "hedge_comfy",
    "apology_first",
    "apology_comfy",
    "features"
]
df = pd.read_csv ('UseofLanguage.csv', names=data_labels)
df.drop(labels="timestamp", axis=1, inplace=True)
print(df.head())