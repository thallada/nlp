import nltk
import random
import re
from textstat.textstat import textstat
#from stat_parser import Parser


class PoemGenerator():
    def __init__(self, corpus):
        #self.sents = corpus.sents('austen-emma.txt')
        self.bigrams = list(nltk.bigrams(corpus.words('shakespeare-hamlet.txt')))
        self.only_punctuation = re.compile(r'[^\w\s]+$')
        self.all_words = [bigram[0] for bigram in self.bigrams
                          if not self.only_punctuation.match(bigram[0])]
        self.cfd = nltk.ConditionalFreqDist(self.bigrams)
        #self.parser = Parser()
        self.history = []

    def markov(self, word, n):
        if n > 0:
            print word,
            n = n - 1
            self.markov(random.choice(self.cfd[word].items())[0], n)
        else:
            print ''

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
        new_syllables = textstat.syllable_count(' '.join(new_line))
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
        first = self.haiku_line([], 0, self.all_words, 5)
        print ' '.join(first)
        next_words = [freq[0] for freq in self.cfd[first[-1]].items()
                      if not self.only_punctuation.match(freq[0])]
        second = self.haiku_line([], 0, next_words, 7)
        print ' '.join(second)
        next_words = [freq[0] for freq in self.cfd[first[-1]].items()
                      if not self.only_punctuation.match(freq[0])]
        third = self.haiku_line([], 0, next_words, 5)
        print ' '.join(third)


if __name__ == '__main__':
    generator = PoemGenerator(nltk.corpus.gutenberg)
    #generator.generate_poem()
    generator.generate_haiku()
