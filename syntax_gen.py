import codecs
import os
import pickle
import random

import spacy

TEMPLATE_CORPUS = 'austencorpus'
CONTENT_CORPUS = 'lovecraftcorpus'

print('Loading spaCy model... ', end='')
nlp = spacy.load('en_core_web_lg')
print('Done')


def load_text_files(dirname):
    for (dirpath, dirnames, filenames) in os.walk(dirname):
        for filename in filenames:
            with codecs.open(os.path.join(dirpath, filename),
                             encoding='utf-8') as f:
                yield f.read()


def load_syntax(dirname):
    full_text = ''
    for text in load_text_files(dirname):
        full_text += text
    return nlp(full_text)


def load_object_to_file(filename):
    with open(filename, 'rb') as f:
        return pickle.load(f)


def save_object_to_file(filename, object):
    with open(filename, 'wb') as f:
        pickle.dump(object, f)


def build_content_dict(content_syntax):
    content_dict = {}
    for word in content_syntax:
        if word.tag not in content_dict:
            content_dict[word.tag] = {}
        if word.dep not in content_dict[word.tag]:
            content_dict[word.tag][word.dep] = set()
        content_dict[word.tag][word.dep].add(word)
    return content_dict


def find_closest_content_word(template_word, content_dict):
    closest = None
    closest_score = 0.0

    if template_word.tag in content_dict:
        if template_word.dep in content_dict[template_word.tag]:
            content_word_set = content_dict[template_word.tag][template_word.dep]
        else:
            random_dep = random.choice(list(content_dict[template_word.tag].keys()))
            content_word_set = content_dict[template_word.tag][random_dep]
    else:
        return None

    for content_word in content_word_set:
        if closest is None or template_word.similarity(content_word) > closest_score:
            closest = content_word
            closest_score = template_word.similarity(content_word)

    return closest


if __name__ == '__main__':
    if os.path.exists('template_syntax.bin'):
        print('Loading parsed template corpus... ', end='')
        template_syntax = spacy.tokens.Doc(spacy.vocab.Vocab())
        template_syntax.from_disk('template_syntax.bin')
        print('Done')
    else:
        print('Parsing template corpus... ', end='')
        template_syntax = load_syntax(TEMPLATE_CORPUS)
        template_syntax.to_disk('template_syntax.bin')
        print('Done')

    if os.path.exists('content_syntax.bin'):
        print('Loading parsed content corpus... ', end='')
        content_syntax = spacy.tokens.Doc(spacy.vocab.Vocab())
        content_syntax.from_disk('content_syntax.bin')
        print('Done')
    else:
        print('Parsing content corpus... ', end='')
        content_syntax = load_syntax(CONTENT_CORPUS)
        content_syntax.to_disk('content_syntax.bin')
        print('Done')

    print('Building content_dict... ', end='')
    content_dict = build_content_dict(content_syntax)
    save_object_to_file('content_dict.bin', content_dict)
    print('Done')

    for template_word in template_syntax[0:100]:
        closest_word = find_closest_content_word(template_word, content_dict)
        if closest_word:
            print(closest_word.text_with_ws, end='')
        else:
            print('<NOMATCH> ', end='')
    import ipdb; ipdb.set_trace()
