""" Defines the Language class, which allows comparisons between documents.

    Written by Colin Hamilton, May 2016
"""
from math import sqrt
from ngramtrie import NGramTrie


def dot_product(lang1, lang2):
    """Returns the sum over all trigrams of lang1 times lang2's frequency"""
    sum = 0
    for key in lang1:
        if key in lang2:
            sum += lang1[key] * lang2[key]
    return sum

def norm(lang1):
    """Returns the norm of the language, ||A|| = sqrt(A*A)"""
    return sqrt(dot_product(lang1, lang1))


class Language:
    """ A language maintains linguistic statistics, and uses them for comparisons.

    In general, a Language object should be created for each language you wish to
    analyze, including for any unknown languages.  Then read_from_file should be
    called for each document you wish to analyze.

    n-grams are currently the mechanism used, so the max size of these n-grams should
    be given when the Language object is created.

    To implement your own preprocessing of files (for example, converting punctuation
    and whitespace, dealing with capital vs lowercase letters), this class can be
    subclassed and the transformation functions customized.

    By default, multiple whitespace and nonalphabetic characters are condensed into
    a single space (' ') character.  Letters are converted to a standard case
    using str.casefold().  This is because, in general, and particularly for small
    documents, these features are not considered useful in distinguishing languages.
    """

    def __init__(self, n=3):
        """Initializes an NGramTrie with the given max size (defaults to 3)"""
        self.n_grams = NGramTrie(n)

# These functions handle transforming characters before counting them.
#   They are intended to be overwritten and customized by subclassing
    def transform(self, char, gram):
        """ Transforms a character read from a document.

        By default, standardizes alphabetic characters with standardize().  Transforms
        nonalphabetic characters with transform_nonalpha().  If it's a space, it's
        added only if the previous n-gram did not end with a space (otherwise
        ignoring the current character).
        This has the effect of condensing multiple nonalphabetic characters into
        a single delimeter between words.
        Args:
            char: The character read from the document
            gram: The previous n-gram extracted from the document

        Returns:
            A string, representing the transformed character.  This is often
            the same as the input character.  It may be the empty string,
            meaning the character should be ignored.
        """
        if not char.isalpha():
            char = self.transform_nonalpha(char)
        if char.isspace() and gram.endswith(char):
            return ""
        else:
            return self.standardize(char)


    def transform_nonalpha(self, char):
        """Called when char is nonalphabetic"""
        return " "


    def standardize(self, char):
        """Called on alphabetic characters, should deal with properties like case"""
        return char.casefold()


    def first_gram(self):
        """Called at the start of a file; returns an initial (typically delimeter) string"""
        return " "


    def last_gram(self):
        """Called at the end of a file; returns a final (typically delimeter) string"""
        return " "


    def read_from_file(self, filename):
        """ Analyses the given file, integrating it into the Language.

        Each character from the file is transformed with the transform() method.
        These characters are then compiled into n-grams, and counted accordingly.
        Args:
            filename: A string with the name of the document to analyse
        """
        trie = self.n_grams
        def _update(gram, char):
            gram = gram + self.transform(char, gram)
            gram = gram[-min(len(gram), trie.n_max):]
            if len(gram) == trie.n_max:
                trie.add(gram)
            return gram

        gram = ""
        for char in self.first_gram():
            gram = _update(gram, char)
        with open(filename, "r") as file:
            for line in file:
                for char in line:
                    gram = _update(gram, char)
            for char in self.last_gram():
                gram = _update(gram, char)
        self.n_grams = trie


    def __str__(self):
        """A string representation of sorted n-gram frequencies of the Language"""
        string = ""
        grams = self.n_grams.frequencies()
        for (gram, freq) in sorted(grams.items(), key=lambda x: x[1]):
            string += "'" + gram + "'  " + str(freq) + "\n"
        return string[:-1]


    def compare(self, other):
        """Compares self to other.

        Args:
            other: Another Language object to compare to.
        Returns:
            A number between 0 and 1 representing how closely correlated
            they are; close to 1 means strong correlation, while close to 0
            means virtually unrelated.  For n=3, two objects of the same language
            will typically have a correlation between 0.8 and 0.95
        """
        lang1 = self.n_grams.frequencies()
        lang2 = other.n_grams.frequencies()
        denom = norm(lang1) * norm(lang2)
        if denom == 0:
            return 0
        else:
            return dot_product(lang1, lang2) / denom

