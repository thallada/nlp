What needs to be improved about this repo:

Generalize and standardize the steps in an NLP pipeline into python classes and
functions. I can think of these off the top of my head:

* Scraper - get text from the internet to local file
* Cleaner - clean raw text of non-corpus text
* Ngramer - assemble text in python list of lists
* Cfdister - restructure data into a conditional frequency distribution
* Other? - restructure data by other metric (rhyming, similarity, etc.)
* Assembler loop - takes structure above and outputs one word
    - Maybe should wrap in a sentence loop, line-by-line loop, paragraph loop,
      etc.

Syntax aware generate is actually pretty bad. I think it forces it to be too
random. The POS tagging is too error prone and fine-detailed.

Ideas for the future:

Pick one or two lines of the haiku from actual haiku or other poems. Then add a
line or two from the corpus (e.g. trump tweets) that both fits the syllables and
rhymes with the end(s) of the real poetic line. I think both sources could be
ngram generated, but I think it would be ideal if they were picked wholesale
from the source. The problem with that approach is that you'd also have to find
a common word between the two source extractions so that the sentence doesn't
abruptly shift between lines. Or, maybe that's a good thing? I guess I should
try both.

Maybe try just switching out the nouns, verbs, adjectives, and adverbs leaving
the rest of the sentence structure largely intact after the tree replace?

Use word similarity vectors to construct a sentence (or poem) around a central
theme. E.g. construct something like the buffalo sentence: syntactically correct
sentences, and maybe even semantically meaningful sentences, but in a totally
novel form because of some arbitrary restriction (can only use the word
"buffalo", or animal words, or onomatopoeias, or etc.).

Integrate alliteration and rhyming.
