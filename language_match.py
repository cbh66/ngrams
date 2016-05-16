""" A set of functions for analyzing groups of languages

    Written by Colin Hamilton, May 2016
"""
from language import Language

def match(unknown, known):
    """ Compares the unknown language with all known languages.

    Args:
        unknown:  A Language object to be compared.
        known:    A dict mapping language names to Language objects.
    Returns:
        A list of tuples of the form (language_name, score), sorted from
        best to worst matches.
    """
    results = [(name, unknown.compare(known[name])) for name in known]
    return sorted(results, key=lambda x: -x[1])


def read_languages(file_dict, n_max):
    """ Creates a set of Language objects with the given languages and files.
    Args:
        file_dict: A dict mapping language names to a list of filenames
        n_max:     The maximum length n-grams for the Languages to track
    Returns:
        A dict mapping language names to Language objects populated with the
        contents of the files specified.
    Notes:
        If a file cannot be read, an error message will be printed, and an
        exception will not be thrown.
    """
    results = {}
    for lang in file_dict:
        results[lang] = Language(n_max)
        for filename in file_dict[lang]:
            try:
                results[lang].read_from_file(filename)
            except Exception:
                print("Could not read file", filename)
    return results


def best_matches(filename, reference_langs, n_max, amt=None):
    """ Finds the closest matches for a document from among a set of Languages.

    Args:
        filename: The name of the file of the document to classify.
        reference_langs: A dict mapping language names to Language objects.
        n_max:    The length of n-grams to classify the unknown document on.
        amt:      The number of results to return (or None, to return all)
    Returns:
        A list of tuples of the form (language_name, score), sorted from
        best to worst matches.  Only the top amt are in the list.
    """
    if amt is None:
        amt = len(reference_langs)
    unknown = Language(n_max)
    unknown.read_from_file(filename)
    comparisons = match(unknown, reference_langs)
    return comparisons[: min(amt, len(comparisons))]
