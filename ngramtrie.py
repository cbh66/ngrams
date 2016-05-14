
def _add_ngram_recursive(ngram, trie, count=1):
        if len(ngram) <= 0: return
        if ngram[0] not in trie:
            trie[ngram[0]] = {"count": 0, "next": {}}
        trie[ngram[0]]["count"] += count
        _add_ngram_recursive(ngram[1:], trie[ngram[0]]["next"], count)

# Largely for debugging; prints a tree representation
def _trie_to_str_recursive(trie, gram_so_far):
    string = ""
    for char in trie:
        string += '"' + gram_so_far + char + '" : ' + str(trie[char]["count"]) + "\n"
        string += _trie_to_str_recursive(trie[char]["next"], gram_so_far + char)
    return string



class NGramTrie:
    # n initializes the max length of n-gram accepted into the trie
    def __init__(self, n):
        self.n_max = n
        self.root = {"count": 0, "next": {}}
        self.counts = [0 for i in range(n + 1)]


    def _add_proper_length_gram(self, ngram, count=1):
        self.root["count"] += count
        for index in range(len(ngram) + 1):
            self.counts[index] += count
        _add_ngram_recursive(ngram, self.root["next"], count)

    # adds a string to the trie the specified number of times.
    # if the string is too long, it will be broken into all possible n-grams,
    #   where n is the n-max of the obejct.
    def add(self, gram, count=1):
        if len(gram) <= self.n_max:
            self._add_proper_length_gram(gram, count)
            return
        # divide up the string into all ngrams
        for start in range(len(gram) - self.n_max + 1):
            self._add_proper_length_gram(gram[start : start + self.n_max], count)



    # returns a list of (string, frequency) tuples from the specified depth
    def _frequencies_recursive(self, trie, depth, goal, gram_so_far):
        if depth == goal:
            return [(gram_so_far, trie["count"] / self.counts[depth])]
        list = []
        for char in trie["next"]:
            list += self._frequencies_recursive(trie["next"][char], depth+1,
                                                goal, gram_so_far + char)
        return list

    # returns a dictionary mapping n-grams to frequencies.  The depth passed is
    #   the length of n-grams to query, and should be between 0 and n_max
    def frequencies(self, depth=-1):
        if depth > self.n_max or depth < 0:
            depth = self.n_max
        return dict(self._frequencies_recursive(self.root, 0, depth, ""))

    def __str__(self):
        return str(self.frequencies(self.n_max))

    def __repr__(self):
        return _trie_to_str_recursive(self.root["next"], "")[:-1]

