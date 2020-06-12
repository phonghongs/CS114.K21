from nltk.corpus import stopwords
from collections import Counter
from os import listdir
import os
import string
import json


def clean_doc(doc):
    tokens = doc.split()

    table = str.maketrans('', '', string.punctuation)
    tokens = [w.translate(table) for w in tokens]

    tokens = [word for word in tokens if word.isalpha()]

    stop_words = set(stopwords.words('english'))
    tokens = [w for w in tokens if not w in stop_words]

    tokens = [word for word in tokens if len(word) > 1]
    return tokens


def add_doc_to_vocab(jsonHL, vocab):
    tokens = clean_doc(jsonHL['headline'])
    vocab.update(tokens)


def process_docs(directory, vocab):
    with open(directory) as json_file:
        for x in json_file:
            y = json.loads(str(x))
            add_doc_to_vocab(y, vocab)


def save_list(lines, filename):
    data = '\n'.join(lines)
    # print(data)
    file = open(filename, 'w')
    file.write(data)
    file.close()

if __name__ == "__main__":
    vocab = Counter()
    process_docs('Sarcasm_Headlines_Dataset_v2.json', vocab)
    process_docs('Sarcasm_Headlines_Dataset.json', vocab)
    print(len(vocab))

    print(vocab.most_common(50))

    min_occurane = 2
    tokens = [k for k,c in vocab.items() if c >= min_occurane]

    save_list(tokens, 'vocab.txt')