import nltk
import operator
import os
import pickle
import random
import re
import codecs
import sys
from nltk.tree import Tree
from collections import defaultdict
from tqdm import tqdm
from stat_parser import Parser

syntaxes = defaultdict(set)
SYNTAXES_FILE = 'syntaxes.p'
CFDS_FILE = 'cfds.p'


def tree_hash(self):
    return hash(tuple(self.leaves()))


Tree.__hash__ = tree_hash


# NOTE: to me: I need to replace nltk parse and tokenization with spacy because it is much faster and less detailed
# which is actually a plus. The problem is that spacy does not create a syntax tree like nltk does. However, it does
# create a dependency tree, which might be good enough for splitting into chunks that can be swapped out between
# corpora. Shitty bus wifi makes it hard to download spacy data and look up the docs.


def generate(filename):
    global syntaxes
    parser = Parser()
    if not os.path.exists(SYNTAXES_FILE):
        #  sents = nltk.corpus.gutenberg.sents('results.txt')
        # NOTE: results.txt is a big file of raw text not included in source control, provide your own corpus.
        with codecs.open(filename, encoding='utf-8') as corpus:
            sents = nltk.sent_tokenize(corpus.read())
            sents = [sent for sent in sents if len(sent) < 150][0:1500]
            for sent in tqdm(sents):
                try:
                    parsed = parser.parse(sent)
                except TypeError:
                    pass
                syntax_signature(parsed, save=True)
        with open(SYNTAXES_FILE, 'wb+') as pickle_file:
            pickle.dump(syntaxes, pickle_file)
    else:
        with open(SYNTAXES_FILE, 'rb+') as pickle_file:
            syntaxes = pickle.load(pickle_file)

    if not os.path.exists(CFDS_FILE):
        with codecs.open(filename, encoding='utf-8') as corpus:
            cfds = [make_cfd(corpus.read(), i, exclude_punctuation=False, case_insensitive=True) for i in range(2, 5)]
            with open(CFDS_FILE, 'wb+') as pickle_file:
                pickle.dump(cfds, pickle_file)
    else:
        with open(CFDS_FILE, 'rb+') as pickle_file:
            cfds = pickle.load(pickle_file)

    sents = nltk.corpus.gutenberg.sents('austen-emma.txt')
    sents = [sent for sent in sents if len(sent) < 50]
    sent = random.choice(sents)
    parsed = parser.parse(' '.join(sent))
    print(parsed)
    print(' '.join(parsed.leaves()))
    replaced_tree = tree_replace(parsed, cfds, [])
    print('=' * 30)
    print(' '.join(replaced_tree.leaves()))
    print(replaced_tree)


def list_to_string(l):
    return str(l).replace(" ", "").replace("'", "")


def syntax_signature(tree, save=False):
    return list_to_string(syntax_signature_recurse(tree, save=save))


def syntax_signature_recurse(tree, save=False):
    global syntaxes
    if type(tree) is Tree:
        label = tree.label()
        if label == ',':
            label = 'COMMA'
        children = [syntax_signature_recurse(child, save=save) for child in tree if type(child) is Tree]
        if not children:
            if save:
                syntaxes[label].add(tree)
            return label
        else:
            if save:
                syntaxes[list_to_string([label, children])].add(tree)
            return [label, children]
    else:
        raise ValueError('Not a nltk.tree.Tree: {}'.format(tree))


def tree_replace(tree, cfds, preceding_children=[]):
    condition_search = ' '.join([' '.join(child.leaves()) for child in preceding_children]).lower()
    sig = syntax_signature(tree)
    if sig in syntaxes:
        matching_fragments = tuple(syntaxes[sig])
        if len(matching_fragments) > 1 and condition_search:
            matching_leaves = [' '.join(frag.leaves()) for frag in matching_fragments]
            most_common = get_most_common(condition_search, cfds)
            candidates = list(set(matching_leaves).intersection(set(most_common)))
            if candidates:
                return Tree(tree.label(), [random.choice(candidates)])
            # find the first element of get_most_common that is also in this list of matching_leaves
        return random.choice(matching_fragments)
    else:
        children = [tree_replace(child, cfds, preceding_children + tree[0:i])
                    for i, child in enumerate(tree) if type(child) is Tree]
        if not children:
            # unable to replace this leaf
            return tree
        else:
            return Tree(tree.label(), children)


# TODO: this part should definitely be in a different class or module. I need to be able to resuse this method
# among all of my nlp expirements. See notes in this repo for more detail.
def make_cfd(text, n, cfd=None, exclude_punctuation=True, case_insensitive=True):
    if not cfd:
        cfd = {}
    if exclude_punctuation:
        nopunct = re.compile('^\w+$')
    sentences = nltk.sent_tokenize(text)
    for sent in sentences:
        sent = nltk.word_tokenize(sent)
        if case_insensitive:
            sent = [word.lower() for word in sent]
        if exclude_punctuation:
            sent = [word for word in sent if nopunct.match(word)]
        for i in range(len(sent) - (n - 1)):
            condition = ' '.join(sent[i:(i + n) - 1])
            sample = sent[(i + n) - 1]
            if condition in cfd:
                if sample in cfd[condition]:
                    cfd[condition][sample] += 1
                else:
                    cfd[condition].update({sample: 1})
            else:
                cfd[condition] = {sample: 1}
    return cfd


def get_most_common(search, cfds, most_common=None):
    if not most_common:
        most_common = list()
    words = search.split(' ')
    for i in reversed(range(len(cfds))):
        n = i + 2
        if len(words) >= (n - 1):
            query = ' '.join(words[len(words) - (n - 1):])
            if query in cfds[i]:
                most_common.extend([entry[0] for entry in sorted(cfds[i][query].items(),
                                                                 key=operator.itemgetter(1),
                                                                 reverse=True)
                                    if entry[0] not in most_common])
    return most_common


if __name__ == '__main__':
    generate(sys.argv[1])
