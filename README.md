# ngrams

## Overview

ngrams is for language analysis.  In particular it is for classifying documents
whose language is unknown.

## How to Use

The accuraccy of the program's analysis depends on its training data.  When
running the program, a source file should be included (or typed in when the
program begins) specifying known languages and example files.  Such a file
should have the form:

    English english1.txt english2.txt
    French  french/
    English english3.txt
    Unknown tbd.txt

Where each line has a language name and the name of 1 or more files written in
that language, or the name of a directory, all of whose files are written in
that language.  If the language name is the 'Unknown' keyword, the document
will be classified.  (A different keyword can be used if the program is invoked
with the -u option).

### Dealing with large training sets

While prediction accuracy is enhanced by large sets of training data, this
can both result in a slow program, and be difficult to manage.

For speed, ngrams offers a caching option, which creates a cache file for each
language.  This way, that language's training data only needs to be read the
first time the program is run; subsequent runs will be much faster.  If the
cache for a language is out of date (ie. a file has been added, deleted, or
modified), the program will automatically recalculate that language's
statistics and update the cache.

Note that this magical cache business has not actually been implemented yet.

To better manage large training sets, it is suggested that you put training
documents in directories whose name is their language.  The source file then
needs only specify the directory, and the program will automatically see
any new or renamed files.

### Other Options

Eventually, I'll try to get a character prediction system in place.  It can
either try to finish a sentence or generate a random string of characters
that should look like it's from the language.  Fun!

## Author

Colin Hamilton, Tufts University

## Acknowledgements

The idea for this program came from the final project for Tufts COMP 11, Fall
2015.  Thanks to Chris Gregg, Bruce Molay, and Ben Hescott.
