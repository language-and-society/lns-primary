import sys
import json
import math

import numpy as np
import matplotlib.pyplot as plt

import enchant
english_dict = enchant.Dict('en_US')

def load_file(movie_name):
    try:
        with open(f"./{movie_name}/{movie_name}_character_data.json") as f:
            character_data = json.load(f)
        return character_data
    except:
        raise FileNotFoundError("movie name not found")

def get_gender():
    gender = input("Enter gender (M/F/all): ").strip()
    if gender not in ['M', 'F', 'all']:
        raise ValueError("Gender not found!")
    return gender

def get_words(character_data=None, gender='all', character='all', language='all', event_split=None):
   
    if event_split == None:
        words = {}
        for key in character_data.keys():
            if character == 'all' or character.lower() == key.lower():
                if character_data[key]['gender'] == gender or gender == 'all':
                    for sentence in character_data[key]['utterances']:
                        for word in sentence.split():
                            if (
                                    language == 'all' 
                                    or (language == 'en' and english_dict.check(word))
                                    or language == 'else'and (not english_dict.check(word))
                                ):
                                try:
                                    words[word.lower()] += 1
                                except:
                                    words[word.lower()] = 1
    else:
        post = False
        words_pre_event = {}
        words_post_event = {}

        for key in character_data.keys():
            if character == 'all' or character.lower() == key.lower():
                if character_data[key]['gender'] == gender or gender == 'all':
                    for sentence in character_data[key]['utterances']:
                        if sentence.lower() == event_split.lower():
                            post = True
                        for word in sentence.split():
                            if (
                                    language == 'all' 
                                    or (language == 'en' and english_dict.check(word))
                                    or language == 'else'and (not english_dict.check(word))
                                ):
                                try:
                                    if post:
                                        words_post_event[word.lower()] += 1
                                    else:
                                        words_pre_event[word.lower()] += 1
                                except:
                                    if post:
                                        words_post_event[word.lower()] = 1
                                    else:
                                        words_pre_event[word.lower()] = 1

    if gender == 'M':
        gender = "male"
    if gender == 'F':
        gender = "female"
    if gender == 'all':
        s = 's'
    else:
        s = ''

    if event_split == None:
        return words, gender, s
    else:
        return words_pre_event, words_post_event, gender, s

def frequency_split(character_data=None, gender='all', movie_name=''):
    
    character = input("Character name (all/etc): ").strip()
    if character == 'all':
        gender = get_gender()
    
    words, gender, s = get_words(character_data, character=character, gender=gender)
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

    character = input("Character name (all/etc): ").strip()
    if character == 'all':
        gender = get_gender()
    
    words, gender, s = get_words(character_data, character=character, gender=gender)
    print(f"Number of unique words for gender {gender}: {len(words)}")

    pronoun_counts = []
    for pronoun in pronouns:
        try:
            pronoun_counts.append(words[pronoun])
        except:
            pronoun_counts.append(0)
    
    _, ax = plt.subplots(figsize=(10, 10))
    ax.pie(pronoun_counts, labels=pronouns, autopct='%1.2f%%')
    plt.title(f"Distribution of pronouns used by {gender} gender{s} in movie {movie_name}")
    plt.show()

def language_split(
        character_data=None,
        gender='all',
        movie_name='',
        event_split=''
    ):
    character = input("Character name (all/etc): ").strip()
    if character == 'all':
        gender = get_gender()

    event_split = input("Enter the event to split by (exact) (if not, hit enter): ")
    
    en_pre_words, en_post_words, gender, s = get_words(
                                                character_data, gender, character, language='en', 
                                                event_split=event_split)
    else_pre_words, else_post_words, gender, s = get_words(
                                                character_data, gender, character, language='else', 
                                                event_split=event_split)
    
    en_words_counter = [sum(en_pre_words.values()), sum(en_post_words.values())]
    else_words_counter = [sum(else_pre_words.values()), sum(else_post_words.values())]

    # NORMALISED, IF they look better :)
    # x1 = sum(en_pre_words.values())
    # y1 = sum(en_post_words.values())
    # x2 = sum(else_pre_words.values())
    # y2 = sum(else_post_words.values())
    # en_words_counter = [x1/(x1+y1), y1/(x1+y1)]
    # else_words_counter = [x2/(x2+y2), y2/(x2+y2)]

    width = 0.3
    
    plt.bar(np.arange(2), en_words_counter, width=width)
    plt.bar(np.arange(2)+width, else_words_counter, width=width)
    if character != 'all':
        plt.title(f"Showing English vs Hindi split before and after the event for charater{s}: {character}")
    else:
        plt.title(f"Showing English vs Hindi split before and after the event for charater{s}: {character} and gender{s}: {gender}")
    plt.show()

if __name__ == "__main__":
    movie_name = input("Enter movie name: ").strip()
    
    # loading data
    character_data = load_file(movie_name)
    gender = 'all'

    while True:
        print("\n\nCHOICES: ")
        print("0. Exit")
        print("1. Change movie")
        print("2. pass")
        print("3. Frequency Counts")
        print("4. Pronoun Split")
        print("5. Language Split")
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
            pass
        elif choice == 3:
            frequency_split(character_data, gender, movie_name)
        elif choice == 4:
            pronoun_split(character_data, gender, movie_name)
        elif choice == 5:
            language_split(character_data, gender, movie_name)