import nltk
import random
from stat_parser import Parser


class PoemGenerator():
    def __init__(self, corpus):
        self.sents = corpus.sents('austen-emma.txt')
        self.bigrams = list(nltk.bigrams(corpus.words('austen-emma.txt')))
        self.cfd = nltk.ConditionalFreqDist(self.bigrams)
        self.parser = Parser()
        self.history = []

    def generate_poem(self):
        sent = random.choice(self.sents)
        parsed = self.parser.parse(' '.join(sent))
        word = random.choice(self.bigrams)[0]
        for i in range(15):
            print word,
            for gram in self.cfd[word].items():
                import ipdb; ipdb.set_trace()  # BREAKPOINT


if __name__ == '__main__':
    generator = PoemGenerator(nltk.corpus.gutenberg)
    print generator.generate_poem()
