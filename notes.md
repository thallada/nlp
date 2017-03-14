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
