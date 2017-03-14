import spacy

nlp = spacy.load('en')
doc = nlp(u'They told us to duck.')

for token in doc:
    print (token.pos_, token.tag_)
