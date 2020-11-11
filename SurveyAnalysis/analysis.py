import pandas as pd
import numpy as np

import matplotlib.pyplot as plt
plt.style.use('seaborn')


df = pd.read_csv('clean_survey_data.csv')

# print(df[:10])
# print(df.groupby(by="gender").sum())
split_df = df.groupby(by="gender").sum()
# print(split_df)

GENDERS = ["Female", "Male", "Non-Binary"]
DATA_LABELS = [
    "hedge_first",
    "hedge_comfy",
    "apology_first",
    "apology_comfy",

    "tag_questions",
    "rising_intonation",
    "empty_adjectives",
    "precise_colours",
    "intensifires",
    "hypercorrect_grammar",
    "superpolite_forms",
    "avoid_slangs",
    "emphatic_stress",
    "hedges",
    "none_of_them"
]

def hedges():
    data_hedge_first = split_df['hedge_first'].to_numpy()
    data_hedge_comfy = split_df['hedge_comfy'].to_numpy()

    WIDTH = 0.9
    ind = np.arange(len(data_hedge_first))
    
    plt.figure(figsize=(20,10))
    
    plt.bar(ind, data_hedge_first, WIDTH/2, color=['orchid', 'dodgerblue', 'purple'], edgecolor='black')
    plt.bar(ind+WIDTH/2, data_hedge_comfy, WIDTH/2, color=['orchid', 'dodgerblue', 'purple'], edgecolor='black')
  
    plt.xticks(ind + WIDTH/4, GENDERS)
    
    plt.xlabel("Genders")
    plt.ylabel("Count")
    plt.title(label="Hedges: First Time VS Comfortable")
    
    # plt.legend(loc='best')
    plt.show()

hedges()