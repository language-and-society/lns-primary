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

def apology():
    data_apology_first = split_df['apology_first'].to_numpy()
    data_apology_comfy = split_df['apology_comfy'].to_numpy()

    WIDTH = 0.9
    ind = np.arange(len(data_apology_first))
    
    plt.figure(figsize=(20,10))
    
    plt.bar(ind, data_apology_first, WIDTH/2, color=['orchid', 'dodgerblue', 'purple'], edgecolor='black')
    plt.bar(ind+WIDTH/2, data_apology_comfy, WIDTH/2, color=['orchid', 'dodgerblue', 'purple'], edgecolor='black')
  
    plt.xticks(ind + WIDTH/4, GENDERS)
    
    plt.xlabel("Genders")
    plt.ylabel("Count")
    plt.title(label="Apology: First Time VS Comfortable")
    
    # plt.legend(loc='best')
    plt.show()

def features(feature, feature_name):
    data = split_df[feature].to_numpy()

    WIDTH = 0.9
    ind = np.arange(len(data))
    plt.figure(figsize=(20,10))
    plt.bar(ind, data, WIDTH/2, color=['orchid', 'dodgerblue', 'purple'], edgecolor='black')
  
    plt.xticks(ind, GENDERS)
    plt.xlabel("Genders")
    plt.ylabel("Count")
    plt.title(label=feature_name)
    plt.show()

hedges()
apology()
features("tag_questions", "Tag Questions: ")
features("rising_intonation", "Rising Intonation: ")
features("empty_adjectives", "Empty Adjectives: ")
features("precise_colours", "Precise Colours: ")
features("intensifires", "Intensifires: ")
features("hypercorrect_grammar", "Hypercorrect Grammar: ")
features("superpolite_forms", "Superpolite Forms: ")
features("avoid_slangs", "Avoid Slangs: ")
features("emphatic_stress", "Emphatic Stress: ")
features("hedges", "Hedges: ")
features("none_of_them", "None of the Features: ")
