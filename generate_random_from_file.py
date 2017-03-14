import nltk
import random
import string
import sys


def main(text):
    bigrams = list(nltk.bigrams(
        [token for token in nltk.word_tokenize(text.decode('utf8'))
         if set(token).difference(set(string.punctuation))]))
    cfdist = nltk.ConditionalFreqDist(bigrams)
    word = random.choice(bigrams)[0]
    for i in range(155):
        print word,
        if i % 3:
            top_words = tuple(cfdist[word])
        else:
            dist = cfdist[word].copy()
            top_words = []
            for i in range(3):
                if dist:
                    top_words.append(dist.max())
                    del dist[top_words[-1]]
                else:
                    break
        word = random.choice(top_words)

if __name__ == '__main__':
    file = sys.argv[1]
    with open(file, 'r') as f:
        main(f.read())
