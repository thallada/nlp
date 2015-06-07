import nltk
import random

TEXT = nltk.corpus.genesis.words('english-kjv.txt')


def main():
    bigrams = nltk.bigrams(TEXT)
    cfdist = nltk.ConditionalFreqDist(bigrams)
    word = random.choice(bigrams)[0]
    for i in range(15):
        print word,
        word = cfdist[word].max()

if __name__ == '__main__':
    main()
