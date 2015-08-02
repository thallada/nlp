import nltk
import random
import re
import string
#import pickle
import csv
import inflect
from count_syllables import count_syllables
#from get_titles import read_titles
#from nltk.corpus import cmudict
#from stat_parser import Parser


class PoemGenerator():
    def __init__(self, corpus):
        #self.corpus = 'melville-moby_dick.txt'
        #self.corpus = read_titles()
        #self.sents = corpus.sents(self.corpus)
        #self.words = corpus.words(self.corpus)
        #self.bigrams = list(nltk.bigrams(self.corpus))
        self.only_punctuation = re.compile(r'[^\w\s]+$')
        self.spaces_and_punctuation = re.compile(r"[\w']+|[.,!?;]")
        #self.all_words = [bigram[0] for bigram in self.bigrams
                          #if not self.only_punctuation.match(bigram[0])]
        #self.cfd = nltk.ConditionalFreqDist(self.bigrams)
        #cfds_file = 'cfds.p'
        #with open(cfds_file, 'rb') as cfds_file:
            #self.cfds = pickle.load(cfds_file)
        #self.cfd = self.cfds[0]
        #self.all_words = list(self.cfd.keys())
        self.sents = []
        self.words = []
        self.all_words = []
        self.inflect_engine = inflect.engine()
        with open('buzzfeed_facebook_statuses.csv', newline='') as statuses:
            reader = csv.reader(statuses, delimiter=',')
            for row in reader:
                if 'via buzzfeed ' not in row[1].lower():  # only English
                    # split title into a list of words and punctuation
                    title = self.spaces_and_punctuation.findall(row[2])
                    # spell out digits into ordinal words for syllable counting
                    title = [string.capwords(
                             self.inflect_engine.number_to_words(int(word)))
                             if word.isdigit() else word for word in title]
                    self.sents.append(title)
                    self.words.extend(title)
                    # all_words only contains words, no punctuation
                    self.all_words.extend([word for word in title
                                           if not
                                           self.only_punctuation.match(word)])
        self.bigrams = list(nltk.bigrams(self.words))
        self.cfd = nltk.ConditionalFreqDist(self.bigrams)
        #self.parser = Parser()
        self.history = []

    def markov(self, word, n):
        if n > 0:
            print(word,)
            n = n - 1
            self.markov(random.choice(self.cfd[word].items())[0], n)
        else:
            print('')

    def generate_poem(self):
        #sent = random.choice(self.sents)
        #parsed = self.parser.parse(' '.join(sent))
        word = random.choice(self.bigrams)[0]
        self.markov(word, 15)

    def haiku_line(self, line, current_syllables, next_words,
                   target_syllables):
        if next_words == []:
            # this branch failed
            return None
        else:
            word = random.choice(next_words)
        new_line = line[:]
        new_line.append(word)
        new_syllables = sum(map(count_syllables, new_line))
        if new_syllables == target_syllables:
            return new_line
        elif new_syllables > target_syllables:
            new_next_words = next_words[:]
            new_next_words.remove(word)
            return self.haiku_line(line, current_syllables, new_next_words,
                                   target_syllables)
        else:
            new_next_words = [freq[0] for freq in self.cfd[word].items()
                              if not self.only_punctuation.match(freq[0])]
            branch = self.haiku_line(new_line, new_syllables, new_next_words,
                                     target_syllables)
            if branch:
                return branch
            else:
                new_next_words = next_words[:]
                new_next_words.remove(word)
                return self.haiku_line(line, current_syllables, new_next_words,
                                       target_syllables)

    def generate_haiku(self):
        haiku = ''
        first = self.haiku_line([], 0, self.all_words, 5)
        haiku = haiku + ' '.join(first) + '\n'
        next_words = [freq[0] for freq in self.cfd[first[-1]].items()
                      if not self.only_punctuation.match(freq[0])]
        second = self.haiku_line([], 0, next_words, 7)
        haiku = haiku + ' '.join(second) + '\n'
        next_words = [freq[0] for freq in self.cfd[second[-1]].items()
                      if not self.only_punctuation.match(freq[0])]
        third = self.haiku_line([], 0, next_words, 5)
        haiku = haiku + ' '.join(third) + '\n'
        return haiku

    def generate_endless_poem(self, previous_line):
        random_syllables = random.choice(range(1, 26))
        if previous_line is None:
            next = self.haiku_line([], 0, self.all_words, random_syllables)
            print(' '.join(next))
        else:
            next_words = [freq[0] for freq in self.cfd[previous_line[-1]].items()
                          if not self.only_punctuation.match(freq[0])]
            next = self.haiku_line([], 0, next_words, random_syllables)
            print(' '.join(next))
        self.generate_endless_poem(next)


if __name__ == '__main__':
    generator = PoemGenerator(nltk.corpus.gutenberg)
    #generator.generate_poem()
    generator.generate_haiku()
    #generator.generate_endless_poem(None)
