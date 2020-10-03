import json

with open('dangal.txt', 'r') as f:
    sentences = f.readlines()

character_data = {}
location_data = {}

def get_type(sentence):
    """
    input:
        sentence:
            a line of text
    output:
        +1 if sentence is specifying location based data
        -1 if sentence is the name of a character (given in all caps)
        0 if continuation of the above two
    """
    if ("INT"  in sentence) or ("EXT" in sentence):
        return 1
    elif sentence.upper() == sentence:
        return -1
    else:
        return 0

def clean_sentence(sentence):
    """
    removes any bracket material from the sentence, 
    along with non-alphanumeric stuff. if anything else is found, we return MISC.
    """
    try:
        sentence = sentence[:sentence.index('(')-1] + sentence[sentence.index(')')+1:]
    except:
        pass

    for word in sentence.split():
        if word.isalnum():
            pass
        else:
            return "MISC"
    return sentence

def match_name(sentence):
    """
    matches and maps the names to singluar elements

    example:
        teenager 1, 2, 3, ... all map to teenager. 
    """
    if "WIFE" in sentence:
        return "WIFE"
    elif "MAHAVIR" in sentence or "FATHER" in sentence or "SINGH" in sentence: 
        return "MAHAVIR"
    elif "TEENAGER" in sentence:
        return "TEENAGER"
    elif "GIRL" in sentence or "WOMAN" in sentence: 
        return "WOMAN"
    elif "GUY" in sentence or "MAN" in sentence or "BROTHER" in sentence: 
        return "MAN"
    elif "COACH" in sentence:
        return "COACH"
    elif "COMMENT" in sentence:
        return "COMMENTATOR"
    elif sentence[-2:] == "ER" or sentence[-3:] == "IAN" or sentence[-2:] == "OR" or sentence[-1:] == "D":
        return "MISC"
    
    return sentence

# initializing the location/character names
prev_character = None
prev_location = None

# go through all the lines in the data
for i in range(len(sentences)):
    # get the sentence
    sentence = sentences[i].strip()
    # get the type: continuation(0) or location(+1) or character(-1)
    sentence_type = get_type(sentence)

    if sentence_type == 1:
        prev_character = None
        prev_location = sentence
    elif sentence_type == -1:
        sentence = match_name(clean_sentence(sentence))
        prev_character = sentence
        prev_location = None
    else:
        if prev_location:
            try:
                location_data[prev_location].append(sentences)
            except:
                location_data[prev_location] = []
        elif prev_character:
            try:
                character_data[prev_character]['utterances'].append(sentence)
            except:
                character_data[prev_character] = {
                    'gender': 'X',
                    'utterances': [],
                }

# prints the names of the characters
for key in character_data.keys():
    print(key)
# # prints the names of the characters
# for key in location_data.keys():
#     print(key)

# writes the utterances data in file
# with open("dangal_character_data.json", 'w') as f:
#     json.dump(character_data, f, indent=4)
# with open("dangal_location_data.json", 'w+') as f:
#     json.dump(location_data, f, indent=4)
