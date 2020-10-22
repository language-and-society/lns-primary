import sys
import json
import math
import matplotlib.pyplot as plt

def load_file(movie_name):
    try:
        with open(f"./{movie_name}/{movie_name}_character_data.json") as f:
            character_data = json.load(f)
        return character_data
    except:
        raise FileNotFoundError("movie name not found")

def get_counts(character_data=None, gender='all', movie_name=''):
    words = {}
    for key in character_data.keys():
        if character_data[key]['gender'] == gender or gender == 'all':
            for sentence in character_data[key]['utterances']:
                for word in sentence.split():
                    try:
                        words[word.lower()] += 1
                    except:
                        words[word.lower()] = 1

    print(f"Number of unique words for gender {gender}: {len(words)}")


    sorted_words = [
        (key, value) for key, value in sorted(
            words.items(), key=lambda item: item[1], reverse=True
        )
    ]

    labels = []
    values = []
    log_values = []
    for item in sorted_words:
        labels.append(item[0])
        values.append(item[1])
        log_values.append((math.log(item[1])))

    if gender == 'M':
        gender = "male"
    if gender == 'F':
        gender = "female"
    
    # WORD COUNT GRAPH
    fig, ax = plt.subplots(figsize=(20, 10))
    ax.bar(labels[:50], values[:50])
    fig.autofmt_xdate()
    plt.title(f"Frequency Distribution of Words by {gender} gender in movie {movie_name}")
    plt.show()

    # log(WORD) COUNT GRAPH
    fig, ax = plt.subplots(figsize=(20, 10))
    ax.bar(labels[:50], log_values[:50])
    fig.autofmt_xdate()
    plt.title(f"Log of frequency Distribution of Words by {gender} gender in movie {movie_name}")
    plt.show()

if __name__ == "__main__":
    movie_name = input("Enter movie name: ").strip()
    
    # loading data
    character_data = load_file(movie_name)

    # get frequency counts
    gender = input("Enter gender (M/F/all): ").strip()
    if gender in ['M', 'F', 'all']:
        get_counts(character_data, gender, movie_name)
    else:
        raise ValueError("Gender not found!")