""" Defines the NGramTrie class, which maintains counts of n-grams.

    Written by Colin Hamilton, May 2016

    TODO:
        - Can actually get rid of n as a necessary property.
            You can just add more count integers if longer grams are put in.
"""


# For the recursive functions, a recursive representation of a trie
#   is defined as follows:  a trie is an object with "count" and "next"
#   keys.  The former is the total number of n-grams counted in the trie.
#   The latter is a dict whose keys are characters and whose values
#   are tries.
def _add_ngram_recursive(ngram, trie, count=1):
    """Adds ngram to trie count times"""
    if len(ngram) <= 0: return
    if ngram[0] not in trie:
        trie[ngram[0]] = {"count": 0, "next": {}}
    trie[ngram[0]]["count"] += count
    _add_ngram_recursive(ngram[1:], trie[ngram[0]]["next"], count)


def _trie_to_str_recursive(trie, gram_so_far):
    """prints a tree representation of a trie; largely for debugging"""
    string = ""
    for char in trie:
        string += '"' + gram_so_far + char + '" : ' + str(trie[char]["count"]) + "\n"
        string += _trie_to_str_recursive(trie[char]["next"], gram_so_far + char)
    return string



class NGramTrie:
    """ An NGramTrie maintains a count of n-grams.

    On creation, an NGramTrie must be initialized with the maximum size of n-grams
    to keep track of.  Once filled, n-gram counts of this size or less can be
    retrieved.  Note the size of an NGramTrie increases roughly exponentially in
    the size of the maximum n.  A max n of no more than 7-9 is recommended.
    """

    def __init__(self, n):
        """ Sets up an NGramTrie with room for n-grams of a specified size

        Args:
            n: An integer representing the maximum size n-grams to store.
        """
        self.n_max = n
        self.root = {"count": 0, "next": {}}
        self.counts = [0 for i in range(n + 1)]


    def _add_proper_length_gram(self, ngram, count=1):
        """Adds the ngram to the trie, assuming it's the proper length"""
        self.root["count"] += count
        for index in range(len(ngram) + 1):
            self.counts[index] += count
        _add_ngram_recursive(ngram, self.root["next"], count)


    def add(self, gram, count=1):
        """Adds a string to the trie the specified number of times.

        If the string is too long, it will be broken into all possible n-grams,
            where n is the n-max of this NGramTrie.

        Args:
            gram: The string consisting of the n-gram(s) to add
            count: The number of times to add the n-gram
        TODO:
            Don't do this breaking up stuff; just increase n_max
        """
        if len(gram) <= self.n_max:
            self._add_proper_length_gram(gram, count)
            return
        # divide up the string into all ngrams
        for start in range(len(gram) - self.n_max + 1):
            self._add_proper_length_gram(gram[start : start + self.n_max], count)


    def _frequencies_recursive(self, trie, depth, goal, gram_so_far):
        """returns a list of (string, frequency) tuples from the specified depth"""
        if depth == goal:
            return [(gram_so_far, trie["count"] / self.counts[depth])]
        list = []
        for char in trie["next"]:
            list += self._frequencies_recursive(trie["next"][char], depth+1,
                                                goal, gram_so_far + char)
        return list


    def frequencies(self, depth=-1):
        """returns a dictionary mapping n-grams to frequencies.

        Args:
            depth: the length of n-grams to query, should be between 0 and n_max
                (otherwise will be set to n_max)
        Returns:
            A dictionary whose keys are the n-grams of the specified length,
                mapped to their frequencies (a number between 0 and 1)
        """
        if depth > self.n_max or depth < 0:
            depth = self.n_max
        return dict(self._frequencies_recursive(self.root, 0, depth, ""))


    def __str__(self):
        """Represents a trie as a dict"""
        return str(self.frequencies(self.n_max))

    def __repr__(self):
        """A tree-like representation of the trie, with its counts"""
        return _trie_to_str_recursive(self.root["next"], "")[:-1]


    def next_most_likely(self, string):
        pass # TODO: go into trie on last n-1 chars, return most likely next one

    def next_random(self, string):
        pass # TODO: like above, but select with uniform number in [0, num-occurences]

