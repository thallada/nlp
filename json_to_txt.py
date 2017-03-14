# Converts a json twitter dump to raw text file.
import codecs
import json
import sys


def get_text_from_json(filename):
    with codecs.open(filename, 'r', 'utf-8') as f:
        return [item['text'] for item in json.loads(f.read())]


def write_text_to_file(filename, text_array, delimiter=' '):
    text_to_write = delimiter.join(text_array)
    with codecs.open(filename, 'w', 'utf-8') as f:
        f.write(text_to_write)


if __name__ == '__main__':
    text_array = get_text_from_json(sys.argv[1])
    write_text_to_file(sys.argv[2], text_array)
