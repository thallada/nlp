"""
My idea here is to encode the entire corpus as one giant two-dimensional numpy array of floats where each row is a
condition word and each column in that row is every other word in the corpus and the probability that the word follows
the conditional word.

This was an interesting idea, but ultimately not that useful since the resulting numpy array is significantly larger
than just storing the CFD in a python dictionary. There might be some crazy linear algebra I could run to compress this
array to make it less sparse. But, I would need to use the same N words for all corpora and I think that the resulting
compressed arrays would only be really useful for comparing with each other to find things like "closeness" between two
corpora as defined by the probabilities that some words follow other words in the text. Also, using the same N words
across all corpora is less awesome because you will miss out on the unique words (names, proper nouns, etc.) present in
only some corpora.
"""
import codecs
import sys
from collections import OrderedDict
from itertools import islice

import nltk  # TODO: write/import a tokenizer so I don't need to import this
import numpy as np


BEGIN_TOKEN = '__BEGIN__'
END_TOKEN = '__END__'


def load_text(filename):
    """Return all text from UTF-8 encoded file on disk."""
    with codecs.open(filename, encoding='utf-8') as corpus:
        return corpus.read()


def build_matrix(text, word_dict, state_size=1):
    matrix = np.zeros((len(word_dict),) * 2, dtype=np.int32)
    sentences = nltk.sent_tokenize(text)
    for sent in sentences:
        sent = [BEGIN_TOKEN] + nltk.word_tokenize(sent) + [END_TOKEN]
        for i in range(len(sent) - (state_size + 1)):
            condition = ' '.join(sent[i:(i + state_size)])
            sample = sent[(i + state_size)]
            condition_index = word_dict[condition]
            sample_index = word_dict[sample]
            matrix[condition_index][sample_index] += 1
    return matrix


def unique_words(tokenized_text, case_insensitive=False):
    """Returns an OrderedDict of all unique words in the given text."""
    word_set = set()
    # TODO: not great that I'm doing tokenization and looping over them twice...
    sentences = nltk.sent_tokenize(text)
    for sent in sentences:
        sent = nltk.word_tokenize(sent)
        for word in sent:
            if case_insensitive:
                word = word.lower()
            word_set.add(word)
    word_set.update(set([BEGIN_TOKEN, END_TOKEN]))
    return OrderedDict((word, i) for i, word in enumerate(sorted(word_set)))


def generate_sentence(matrix, word_dict):
    sent = []
    counter = 0
    choices = np.arange(len(word_dict))
    # Is it bad to create a new array in the inner loop down there?
    #  probs = np.zeros((len(word_dict),), dtype=np.float)
    state = word_dict[BEGIN_TOKEN]
    # TODO: it's not finding the end token
    while state != word_dict[END_TOKEN] and counter != 30:
        probs = matrix[state].astype(np.float)
        probs /= probs.sum()
        state = np.random.choice(choices, p=probs)
        if state != word_dict[END_TOKEN]:
            sent.append(next(islice(word_dict.items(), int(state), None))[0])
        counter += 1
    return ' '.join(sent)


if __name__ == '__main__':
    text = load_text(sys.argv[1])
    word_dict = unique_words(text)
    matrix = build_matrix(text, word_dict)
    print(generate_sentence(matrix, word_dict))
