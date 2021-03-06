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

def get_sentences(character_data=None, gender='all', character='all', language='all'):
    sentences = []
    for key in character_data.keys():
        if character == 'all' or character.lower() == key.lower():
            if character_data[key]['gender'] == gender or gender == 'all':
                for sentence in character_data[key]['utterances']:
                    flag = True 
                    for word in sentence.split():
                        if not (
                                language == 'all' 
                                or (language == 'en' and english_dict.check(word))
                                or language == 'else'and (not english_dict.check(word))
                            ):
                            flag = False
                            break
                    
                    if flag:
                        sentences.append(sentence.lower())
    if gender == 'M':
        gender = "male"
    if gender == 'F':
        gender = "female"
    if gender == 'all':
        s = 's'
    else:
        s = ''
    return sentences, gender, s

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
    if character == 'all':
        plt.title(f"Frequency Distribution of Words by {gender} gender{s} in movie {movie_name}")
    else:
        plt.title(f"Frequency Distribution of Words for {character} in movie {movie_name}")
    plt.show()

    # log(WORD) COUNT GRAPH
    fig, ax = plt.subplots(figsize=(20, 10))
    ax.bar(labels[:50], log_values[:50])
    fig.autofmt_xdate()
    if character == 'all':
        plt.title(f"Log(Frequency Distribution) of Words by {gender} gender{s} in movie {movie_name}")
    else:
        plt.title(f"Log(Frequency Distribution) of Words for {character} in movie {movie_name}")    
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
    if character == 'all':
        plt.title(f"Pronoun Split by {gender} gender{s} in movie {movie_name}")
    else:
        plt.title(f"Pronoun Split for {character} in movie {movie_name}")     
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
    if event_split == '':
        event_split=None
        en_words, gender, s = get_words(character_data, gender, character, language='en', event_split=event_split)
        else_words, gender, s = get_words(character_data, gender, character, language='else', event_split=event_split)
        
        count_en_words = sum(en_words.values())
        count_else_words = sum(else_words.values())
        
        plt.bar(np.arange(2), [count_en_words, count_else_words])
        plt.title(f"Showing English vs Hindi split for charater{s}: {character} and gender{s}: {gender}")
        plt.show()
        return
    
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

def sentence_language_split(character_data=None, gender='all', movie_name=''):
    character = input("Character name (all/etc): ").strip()
    if character == 'all':
        gender = get_gender()
    # len_all_sentences = len(get_sentences(character_data, gender, character, language='all'))
    en_sentences, gender, s = get_sentences(character_data, gender, character, language='en')
    else_sentences, gender, s = get_sentences(character_data, gender, character, language='else')

    # print(en_sentences)

    plt.bar(np.arange(2), [len(en_sentences), len(else_sentences)])

    if character == 'all':
        plt.title(f"Showing pure English vs Hindi sentence split for all charaters and gender{s}: {gender}")
    else:
        plt.title(f"Showing pure English vs Hindi sentence split for charater: {character}")
    plt.show()
    return

def compare_questions(character_data=None, gender='all', movie_name=''):
    # character = input("Character name (all/etc): ").strip()
    # if character == 'all':
    #     gender = get_gender()

    # USING SENTENCES
    # NOTE: these are list, str, char resp
    male_sentences, gender, s = get_sentences(character_data, gender='M', language='all')
    female_sentences, gender, s = get_sentences(character_data, gender='F', language='all')

    # USING WORDS
    # NOTE: these are dict, str, char resp
    # words, gender, s = get_words(character_data, character=character, gender=gender)

    #######################################################################
    ############################# INSRERT LOGIC ###########################
    #######################################################################

    check_words = [
        "?",
        "mujhey lagta",
        "mujhe lagta",
        "mein soch",
    ]

    male_count = 0
    female_count = 0

    for sentence in male_sentences:
        flag = False
        for word in check_words:
            if word in sentence:
                flag = True
                break
        if flag:
            male_count += 1

    for sentence in female_sentences:
        flag = False
        for word in check_words:
            if word in sentence:
                flag = True
                break
        if flag:
            female_count += 1

        plt.bar(np.arange(2), [male_count, female_count])

    plt.title(f"Male VS female occurances of questions for {movie_name}")
    plt.show()
    return

def compare_apology(character_data=None, gender='all', movie_name=''):
    # character = input("Character name (all/etc): ").strip()
    # if character == 'all':
    #     gender = get_gender()

    male_sentences, gender, s = get_sentences(character_data, gender='M', language='all')
    female_sentences, gender, s = get_sentences(character_data, gender='F', language='all')

    check_words = [
        "maaf",
        "maf",
        "mafi",
        "sorry"
    ]

    male_count = 0
    female_count = 0

    for sentence in male_sentences:
        flag = False
        for word in check_words:
            if word in sentence:
                flag = True
                break
        if flag:
            male_count += 1

    for sentence in female_sentences:
        flag = False
        for word in check_words:
            if word in sentence:
                flag = True
                break
        if flag:
            female_count += 1

        plt.bar(np.arange(2), [male_count, female_count])

    plt.title(f"Male VS female occurances of apology for {movie_name}")
    plt.show()
    return

def compare_slang(character_data=None, gender='all', movie_name=''):
    # character = input("Character name (all/etc): ").strip()
    # if character == 'all':
    #     gender = get_gender()

    male_sentences, gender, s = get_sentences(character_data, gender='M', language='all')
    female_sentences, gender, s = get_sentences(character_data, gender='F', language='all')

    check_words = [
        "saale",
        "bavdi",
        "bavri",
        "baavdi",
        "sala",
        "sale",
        "kutte",
        "kutti",
        "kutton",
        "kutiya",
        "kamine",
        "kamini",
        "chutiye",
        "harami",
        "fuck",
        "fukra",
        "sex",
    ]

    male_count = 0
    female_count = 0

    for sentence in male_sentences:
        flag = False
        for word in check_words:
            if word in sentence:
                flag = True
                break
        if flag:
            male_count += 1

    for sentence in female_sentences:
        flag = False
        for word in check_words:
            if word in sentence:
                flag = True
                break
        if flag:
            female_count += 1

        plt.bar(np.arange(2), [male_count, female_count])

    plt.title(f"Male VS female occurances of slangs for {movie_name}")
    plt.show()
    return

if __name__ == "__main__":
    movie_name = input("Enter movie name: ").strip()
    
    # loading data
    character_data = load_file(movie_name)
    gender = 'all'

    while True:
        print("\n\nCHOICES: ")
        print("0. Exit")
        print("1. Change movie")
        print("2. Frequency Counts")
        print("3. Pronoun Split")
        print("4. Language Split")
        print("5. Sentence Language Split")
        print("6. Lakoff: questions")
        print("7. Lakoff: apologies")
        print("8. Lakoff: slangs")
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
            frequency_split(character_data, gender, movie_name)
        elif choice == 3:
            pronoun_split(character_data, gender, movie_name)
        elif choice == 4:
            language_split(character_data, gender, movie_name)
        elif choice == 5:
            sentence_language_split(character_data, gender, movie_name)
        elif choice == 6:
            compare_questions(character_data, gender, movie_name)
        elif choice == 7:
            compare_apology(character_data, gender, movie_name)
        elif choice == 8:
            compare_slang(character_data, gender, movie_name)
