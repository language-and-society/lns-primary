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

def get_words(character_data=None, gender='all'):
    words = {}
    for key in character_data.keys():
        if character_data[key]['gender'] == gender or gender == 'all':
            for sentence in character_data[key]['utterances']:
                for word in sentence.split():
                    try:
                        words[word.lower()] += 1
                    except:
                        words[word.lower()] = 1
    
    if gender == 'M':
        gender = "male"
    if gender == 'F':
        gender = "female"
    if gender == 'all':
        s = 's'
    else:
        s = ''

    return words, gender, s

def frequency_split(character_data=None, gender='all', movie_name=''):
    words, gender, s = get_words(character_data, gender)
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
    
    # WORD COUNT GRAPH
    fig, ax = plt.subplots(figsize=(20, 10))
    ax.bar(labels[:50], values[:50])
    fig.autofmt_xdate()
    plt.title(f"Frequency Distribution of Words by {gender} gender{s} in movie {movie_name}")
    plt.show()

    # log(WORD) COUNT GRAPH
    fig, ax = plt.subplots(figsize=(20, 10))
    ax.bar(labels[:50], log_values[:50])
    fig.autofmt_xdate()
    plt.title(f"Log of frequency Distribution of Words by {gender} gender{s} in movie {movie_name}")
    plt.show()

def pronoun_split(
        character_data=None, 
        gender='all', 
        movie_name='', 
        pronouns=['tu', 'tum', 'aap', 'you']
    ):
    words, gender, s = get_words(character_data, gender)
    print(f"Number of unique words for gender {gender}: {len(words)}")

    pronoun_counts = []
    for pronoun in pronouns:
        try:
            pronoun_counts.append(words[pronoun])
        except:
            pronoun_counts.append(0)
    
    fig, ax = plt.subplots(figsize=(10, 10))
    ax.pie(pronoun_counts, labels=pronouns, autopct='%1.2f%%')
    plt.title(f"Distribution of pronouns used by {gender} gender{s} in movie {movie_name}")
    plt.show()


if __name__ == "__main__":
    movie_name = input("Enter movie name: ").strip()
    
    # loading data
    character_data = load_file(movie_name)

    # getting gender
    gender = input("Enter gender (M/F/all): ").strip()
    if gender not in ['M', 'F', 'all']:
        raise ValueError("Gender not found!")

    while True:
        print("\n\nCHOICES: ")
        print("0. Exit")
        print("1. Change movie")
        print("2. Change gender")
        print("3. Frequency Counts")
        print("4. Pronoun Split")
        print("\n")
        try:
            choice = int(input("Enter choice: ").strip())
        except KeyboardInterrupt:
            break
        except:
            break

        if not choice:
            break
        elif choice == 1:
            movie_name = input("Enter movie name: ").strip()
            character_data = load_file(movie_name)
        elif choice == 2:
            new_gender = input("Enter gender (M/F/all): ").strip()
            if new_gender not in ['M', 'F', 'all']:
                print("Gender not found!")
            else:
                gender = new_gender
        elif choice == 3:
            frequency_split(character_data, gender, movie_name)
        elif choice == 4:
            pronoun_split(character_data, gender, movie_name)