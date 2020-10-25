from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt
import pandas as pd
import json

with open('dangal_character_data.json') as f:
  data = json.load(f)

comment_words = ''
stopwords = set(STOPWORDS)

hi_stopwords = {'Andar', 'at', 'adi', 'ap', 'apanaa', 'apani', 'apanee', 'apane', 'abhi', 'abhee', 'aadi', 'aap', 'inhin', 'inhen', 'inhon', 'itayaadi', 'ityaadi', 'in', 'inakaa', 'inheen', 'inhen', 'inhon', 'is', 'isakaa', 'isaki', 'isakee', 'isake', 'isamen', 'isi', 'isee', 'ise', 'unhin', 'unhen', 'unhon', 'un', 'unakaa', 'unaki', 'unakee', 'unake', 'unako', 'unheen', 'unhen', 'unhon', 'us', 'usake', 'usi', 'usee', 'use', 'ek', 'evn', 'es', 'ese', 'aise', 'or', 'aur', 'ka_i', 'ka_ii', 'kar', 'karataa', 'karate', 'karanaa', 'karane', 'karen', 'kahate', 'kahaa', 'kaa', 'kaafi', 'kaaphee', 'ki', 'kinhen', 'kinhon', 'kitanaa', 'kinhen', 'kinhon', 'kiyaa', 'kir', 'kis', 'kisi', 'kisee', 'kise', 'kee', 'kuchh', 'kul', 'ke', 'ko', 'koi', 'koii', 'kon', 'konasaa', 'kaun', 'kaunasaa', 'gayaa', 'ghar', 'jab', 'jahaan', 'jahaan', 'jaa', 'jinhen', 'jinhon', 'jitanaa', 'jidhar', 'jin', 'jinhen', 'jinhon', 'jis', 'jise', 'jeedhar', 'jesaa', 'jese', 'jaisaa', 'jaise', 'jo', 'tak', 'tab', 'tarah', 'tinhen', 'tinhon', 'tin', 'tinhen', 'tinhon', 'tis', 'tise', 'to', 'thaa', 'thi', 'thee', 'the', 'dabaaraa', 'davaaraa', 'diyaa', 'dusaraa', 'dusare', 'doosare', 'do', 'dvaaraa', 'n', 'nahin', 'naheen', 'naa', 'niche', 'nihaayat', 'neeche', 'ne', 'par', 'pahale', 'puraa', 'pooraa', 'pe', 'fir', 'bani', 'banee', 'bahi', 'bahee', 'bahut', 'baad', 'baalaa', 'bilakul', 'bhi', 'bhitar', 'bhee', 'bheetar', 'magar', 'maano', 'me', 'men', 'yadi', 'yah', 'yahaan', 'yahaan', 'yahi', 'yahee', 'yaa', 'yih', 'ye', 'rakhen', 'ravaasaa', 'rahaa', 'rahe', 'rvaasaa', 'lie', 'liye', 'lekin', 'v', 'vagerah', 'varag', 'varg', 'vah', 'vahaan', 'vahaan', 'vahin', 'vaheen', 'vaale', 'vuh', 've', 'vagairah', 'sng', 'sakataa', 'sakate', 'sabase', 'sabhi', 'sabhee', 'saath', 'saabut', 'saabh', 'saaraa', 'se', 'so', 'hi', 'hee', 'hua', 'huaa', 'hui', 'huii', 'hue', 'he', 'hen', 'hai', 'hain', 'ho', 'hotaa', 'hoti', 'hotee', 'hote', 'honaa', 'hone'}

stopwords = stopwords.union(hi_stopwords);

for key in data.keys():
    for val in data[key]['utterances']:

        val = str(val)
        tokens = val.split()
        for i in range(len(tokens)):
            tokens[i] = tokens[i].lower()

        comment_words += " ".join(tokens)+" "

    wordcloud = WordCloud(width = 800, height = 800,
                    background_color ='white',
                    stopwords = stopwords,
                    min_font_size = 10).generate(comment_words)

    filename = "wordclouds/" + key + "_wordcloud.png"

    plt.figure(figsize = (8, 8), facecolor = None)
    plt.imshow(wordcloud)
    plt.axis("off")
    plt.tight_layout(pad = 0)

    plt.savefig(filename)
