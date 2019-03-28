'''
    Name: Sumanth Doddapaneni
    Roll: 20160020125
    Last Update:
    Work: "Key term extarction from a single doc"
'''

# importing req libraries
from nltk.stem import WordNetLemmatizer
from nltk.stem.porter import *


def keyword_extract(text,stopwords):
# lemantizing to remove multiple occurances of similar words
    lemmatiser = WordNetLemmatizer()
    stemmer = PorterStemmer()


    # creating dictionary for the frequencies of words
    word_freq = {}
    text_str = ' '.join(text)
    for word in text_str.split():
        word = word.lower()
        if word not in stopwords:
            #word = structure(word)
            word = lemmatiser.lemmatize(word, pos="v")
            #word = stemmer.stem(word)
            if word not in word_freq:
                word_freq[word] = 1
            else:
                word_freq[word] += 1

    sorted_word_freq = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)
    # print(sorted_word_freq)

    # top 10 frequent words list
    freq_words = []
    for k, v in sorted_word_freq:
        if len(freq_words) <= 10:
            freq_words.append(k)


    cooc_matrix = {}
    for key in word_freq:
        cooc_matrix[key] = {}

    # creating dictionary
    def create_cooc_matrix(text):
        for key in word_freq:


            text = [x.strip() for x in text]
            words = []
            for line in text:
                line = line.lower()
                words = line.split()
                if key in words:
                    words.remove(key)
                    for word in words:
                        #word = structure(word)
                        if word in cooc_matrix[key].keys():
                            cooc_matrix[key][word] += 1
                        else:
                            cooc_matrix[key][word] = 1
    create_cooc_matrix(text)


    X2_dict = {}
    def X2_test():
        for key in word_freq:
            X2 = 0
            nw = sum(cooc_matrix[key].values())
            if nw < 2:
                continue
            for word in freq_words:
                pg = sum(cooc_matrix[word].values()) / len(word_freq)
                try:
                    freq_w_g = cooc_matrix[key][word]
                except:
                    freq_w_g = 0
                X2 += (freq_w_g - (nw * pg))**2 / (nw * pg)
                X2_dict[key] = X2

    X2_test()
    sorted_dict = sorted(X2_dict.items(), key=lambda x: x[1], reverse=True)
    return sorted_dict
