
from language import Language

def match(unknown, known):
    results = [(name, unknown.compare(known[name])) for name in known]
    return sorted(results, key=lambda x: -x[1])

# file_dict is an object mapping language names to lists of filenames
def read_languages(file_dict, n_max):
    results = {}
    for lang in file_dict:
        results[lang] = Language(n_max)
        for filename in file_dict[lang]:
            results[lang].read_from_file(filename)
    return results

def best_matches(filename, reference_langs, n_max, amt=None):
    if amt is None:
        amt = len(reference_langs)
    unknown = Language(n_max)
    unknown.read_from_file(filename)
    comparisons = match(unknown, reference_langs)
    return comparisons[ : min(amt, len(comparisons))]
