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
# print(df['features'].head(100).tail(5))
# DONE PREP



# GROUPING DATA
# print(df.loc[df['gender'] == 'Male'].head())

# GETTING FEATURES
features = [
    "Tag questions, e.g. she’s very nice, isn’t she?",
    "Rising intonation on declaratives, e.g. it’s really good?",
    "‘Empty’ adjectives, e.g. divine, charming, cute.",
    "Precise color terms, e.g. magenta, aquamarine",
    "Intensifiers such as just and so, e.g. I like him so much.",
    "‘Hypercorrect’ grammar, e.g. consistent use of standard verb forms. Eg. 'Whom are we inviting to the party?' instead of 'Who are we inviting to the party?'",
    "‘Superpolite’ forms, e.g. indirect requests, euphemisms. Eg: 'dear departed' instead of 'dead', 'letting someone go' instead of 'firing an employee'",
    "Avoidance of strong swear words, e.g. fudge, my goodness.",
    "Emphatic stress, e.g. it was a BRILLIANT performance.",
    "Lexical hedges or fillers, e.g. you know, sort of, well, you see.",
    "I do not use any of the above features in my language",
]

# USING FEATURES
all_data_labels = [
    "gender", 
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


labels_dict = {}

for label, desc in zip(all_data_labels[-len(features): ], features):
    labels_dict[desc] = label

new_df = pd.DataFrame(columns=all_data_labels)

# print(len(df))
for i in range(len(df)):
    feature_values = []
    for feature in data_labels[1: -1]:
        # print(feature, df.loc[i][feature], type(df.loc[i][feature]))
        feature_values.append(df.loc[i][feature])
    
    # print(feature_values)
    # print()

    extracted_labels = []
    try:
        for desc in df.loc[i]['features'].split(";"):
            extracted_labels.append(labels_dict[desc])
    except:
        pass

    for actual_label in all_data_labels[-len(features):]:
        if actual_label in extracted_labels:
            feature_values.append(1)
        else:
            feature_values.append(0)


    final_dict = {}
    for i, j in zip(all_data_labels, feature_values):
        final_dict[i] = j
    
    # print(final_dict)
    new_df = new_df.append(final_dict, ignore_index=True)


# print(new_df.head(5))
# print(len(new_df))

new_df.to_csv('new_clean_survey_data.csv', index=False)