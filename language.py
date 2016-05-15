
from ngramtrie import NGramTrie
from math import sqrt


def dot_product(lang1, lang2):
    sum = 0
    for key in lang1:
        if key in lang2:
            sum += lang1[key] * lang2[key]
    return sum

def norm(lang1):
    return sqrt(dot_product(lang1, lang1))


class Language:
    def __init__(self, n=3):
        self.n_grams = NGramTrie(n)

# These functions handle transforming characters before counting them.
#   They are intended to be overwritten and customized by subclassing

# The transform function is called once for each character read from the
#   input, and should return a string, to transform the given character to.
#   Typically this is a single character, and most of the time is the same
#   as the character passed in.  A return value of the empty string indicates
#   nothing being appended, ie. the character is ignored.  An extra space is
#   added before the start and at the end of each file.
    def transform(self, char, gram):
        if not char.isalpha():
            char = self.transform_space(char)
        if char.isspace() and gram.endswith(char):
            return ""
        else:
            return self.standardize(char)

    def transform_space(self, char):
        return " "

    def standardize(self, char):
        return char.casefold()

    def first_gram(self):
        return " "

    def last_gram(self):
        return " "

    def read_from_file(self, filename):
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
        string = ""
        grams = self.n_grams.frequencies()
        for (gram, freq) in sorted(grams.items(), key=lambda x: x[1]):
            string += "'" + gram + "'  " + str(freq) + "\n"
        return string[:-1]

    def compare(self, other):
        lang1 = self.n_grams.frequencies()
        lang2 = other.n_grams.frequencies()
        return dot_product(lang1, lang2) / (norm(lang1) * norm(lang2))



