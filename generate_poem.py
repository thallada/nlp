import codecs
import nltk
import random
import re
import string
import csv
import inflect
from count_syllables import count_syllables


class PoemGenerator(object):
    def __init__(self, corpus='buzzfeed_facebook_statues.csv'):
        self.only_punctuation = re.compile(r'[^\w\s]+$')
        self.spaces_and_punctuation = re.compile(r"[\w']+|[.,!?;]")
        self.sents = []
        self.words = []
        self.all_words = []
        self.inflect_engine = inflect.engine()
        self.read_corpus(corpus)
        self.bigrams = list(nltk.bigrams(self.words))
        self.cfd = nltk.ConditionalFreqDist(self.bigrams)
        self.history = []

    def read_corpus(self, corpus):
        """Given filename of corpus, populate words, all_words, and sents."""
        if corpus.endswith('.csv'):
            if 'buzzfeed_facebook_statuses' in corpus:
                return self.read_buzzfeed_corpus(corpus)
            else:
                return self.read_csv_corpus(corpus)
        elif corpus.endswith('.txt'):
            return self.read_txt_corpus(corpus)
        else:
            raise TypeError(('Unrecognized corpus file type: %s.' % corpus) +
                            '".txt" and ".csv" are only supported')

    def read_txt_corpus(self, corpus):
        with codecs.open(corpus, 'r', 'utf-8') as corpus_content:
            text = corpus_content.read()
            sents = nltk.tokenize.sent_tokenize(text)
            words = nltk.tokenize.word_tokenize(text)
            self.sents.extend(sents)
            self.words.extend(words)
            self.all_words.extend([word for word in words
                                   if not
                                   self.only_punctuation.match(word)])

    def read_csv_corpus(self, corpus):
        raise NotImplementedError('Haven\'t implemented generic csv reading')

    def read_buzzfeed_corpus(self, corpus):
        with open(corpus, newline='', encoding='utf-8') as statuses:
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

    def markov(self, word, n):
        if n > 0:
            print(word,)
            n = n - 1
            self.markov(random.choice(self.cfd[word].items())[0], n)
        else:
            print('')

    def generate_text(self):
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
        if not next_words:
            next_words = self.all_words
        second = self.haiku_line([], 0, next_words, 7)
        haiku = haiku + ' '.join(second) + '\n'
        next_words = [freq[0] for freq in self.cfd[second[-1]].items()
                      if not self.only_punctuation.match(freq[0])]
        if not next_words:
            next_words = self.all_words
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
    generator = PoemGenerator(corpus='buzzfeed_facebook_statuses.csv')
    haiku = generator.generate_haiku()
    print(haiku)
