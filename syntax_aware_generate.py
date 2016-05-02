import os
import pickle
import random
import nltk
from nltk.tree import Tree
from collections import defaultdict
from tqdm import tqdm
from stat_parser import Parser

syntaxes = defaultdict(set)
SYNTAXES_FILE = 'syntaxes.p'


def tree_hash(self):
    return hash(tuple(self.leaves()))

Tree.__hash__ = tree_hash


def generate():
    global syntaxes
    parser = Parser()
    if not os.path.exists(SYNTAXES_FILE):
        sents = nltk.corpus.gutenberg.sents('melville-moby_dick.txt')
        sents = sents[0:100]
        for sent in tqdm(sents):
            try:
                parsed = parser.parse(' '.join(sent))
            except TypeError:
                pass
            syntax_signature(parsed, save=True)
        with open(SYNTAXES_FILE, 'wb+') as pickle_file:
            pickle.dump(syntaxes, pickle_file)
    else:
        with open(SYNTAXES_FILE, 'rb+') as pickle_file:
            syntaxes = pickle.load(pickle_file)
    sents = nltk.corpus.gutenberg.sents('austen-emma.txt')
    sent = random.choice(sents)
    parsed = parser.parse(' '.join(sent))
    print(parsed)
    print(' '.join(parsed.leaves()))
    replaced_tree = tree_replace(parsed)
    print('='*30)
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


def tree_replace(tree):
    sig = syntax_signature(tree)
    if sig in syntaxes:
        return random.choice(tuple(syntaxes[sig]))
    else:
        children = [tree_replace(child) for child in tree if type(child) is Tree]
        if not children:
            # unable to replace this leaf
            return tree
        else:
            return Tree(tree.label(), children)


if __name__ == '__main__':
    generate()
