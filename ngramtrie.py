""" Defines the NGramTrie class, which maintains counts of n-grams.

    Written by Colin Hamilton, May 2016

    TODO:
        - Can actually get rid of n as a necessary property.
            You can just add more count integers if longer grams are put in.
"""

import random

# For the recursive functions, a recursive representation of a trie
#   is defined as follows:  a trie is an object with "count" and "next"
#   keys.  The former is the total number of n-grams counted in the trie.
#   The latter is a dict whose keys are characters and whose values
#   are tries.

def _trie_at(string, trie):
    """Goes into the trie, returns sub-trie at the given string, or None"""
    if len(string) <= 0:
        return trie
    if string[0] not in trie["next"]:
        #print(string[0], trie)
        return None
    return _trie_at(string[1:], trie["next"][string[0]])


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


def weighted_random(probabilities):
    if sum(probabilities.values()) <= 0:    # If all are zero, make all equally likely
        new_probs = {}
        for key in probabilities:
            new_probs[key] = 1
        probabilities = new_probs
    index = random.randint(0, sum(probabilities.values()))
    for key in probabilities:
        index -= probabilities[key]
        if index <= 0:
            return key
    return None        # Should never get here




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


    def _counts_recursive(self, trie, depth_goal, gram_so_far):
        """returns a list of (string, count) tuples from the specified depth"""
        if depth_goal <= 0:
            return [(gram_so_far, trie["count"])]
        list = []
        for char in trie["next"]:
            list += self._counts_recursive(trie["next"][char], depth_goal - 1,
                                            gram_so_far + char)
        return list


    def gram_counts(self, depth=-1):
        if depth > self.n_max or depth < 0:
            depth = self.n_max
        return dict(self._counts_recursive(self.root, depth, ""))



    def __str__(self):
        """Represents a trie as a dict"""
        return str(self.frequencies(self.n_max))

    def __repr__(self):
        """A tree-like representation of the trie, with its counts"""
        return _trie_to_str_recursive(self.root["next"], "")[:-1]



    def next_most_likely(self, string):
        trie = None
        num_chars = min(len(string), self.n_max - 1)
        while trie is None and num_chars >= 0:
            trie = _trie_at(string[-num_chars:], self.root)
            num_chars -= 1
        if trie is None:  # No prediction can be made
            return ""
        probabilities = {}
        for key in trie["next"]:
            if trie["next"][key] is None:
                probabilities[key] = 0
            else:
                probabilities[key] = trie["next"][key]["count"]
        return weighted_random(probabilities)


    def next_random(self, string):
        trie = None
        num_chars = min(len(string), self.n_max - 1)
        while (not trie or not trie["next"]) and num_chars >= 0:
            substr = "" if num_chars == 0 else string[-num_chars:]
            trie = _trie_at(substr, self.root)
            num_chars -= 1
        if not trie or not trie["next"]:  # No prediction can be made
            return ""
        probabilities = {}
        for key in trie["next"]:
            if trie["next"][key] is None:
                probabilities[key] = 0
            else:
                probabilities[key] = trie["next"][key]["count"]
        result = weighted_random(probabilities)
        return result

