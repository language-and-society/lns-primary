import json

with open('pink.txt', 'r', encoding="utf8") as f:
    sentences = f.readlines()

character_data = {}
location_data = {}

def get_type(sentence):
    if ("INT"  in sentence) or ("EXT" in sentence) or ':' in sentence or '-' in sentence or '–' in sentence or '(' in sentence or ')' in sentence or 'TH' in sentence or '!' in sentence or '.' in sentence:
        return 1
    elif sentence.upper() == sentence:
        return -1
    else:
        return 0

def clean_sentence(sentence):
    try:
        return (sentence[:sentence.index('(')-1] + sentence[sentence.index(')')+1:])
    except:
        return sentence

def match_name(sentence):
    return sentence

prev_character = None
prev_location = None

for i in range(len(sentences)):
    sentence = sentences[i].strip()
    sentence_type = get_type(sentence)

    if sentence_type == 1:
        prev_character = None
        prev_location = sentence
    elif sentence_type == -1:
        sentence = clean_sentence(sentence)
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

for key in character_data.keys():
    print(key)

with open("pink_character_data.json", 'w') as f:
    json.dump(character_data, f, indent=4)

# with open("dangal_location_data.json", 'w+') as f:
#     json.dump(location_data, f, indent=4)
