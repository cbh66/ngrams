""" A program for classifying languages

    Written by Colin Hamilton, May 2016

    Inspired by the Tufts University COMP 11 Final project "trigrams", Fall 2015

    TODO:
    - Allow wildcards and such in filenames.  See expanduser(), expandvars(), glob
    - Add caching for speedup (either single files, by language, or by directory)
        - Need to figure out when to use cache, when to update
        - Is a hybrid system possible?  Have cache keep track of filenames;
            check them off if they're in cache, else read these new files
            - Gotta make sure to minimize risk of accidental duplication of data,
                ie having a file's data in cache and then reading it again in
                addition to that
            - Could keep filenames/last modified date to see if it's up to date
            - Would need a hard refresh option, probably one for individual
                languages, and one to refresh all languages
    - Add option for directory traversal
    - Implement prediction -- language name, optional "seed", num letters to
        predict, choose randomized or max likelihood (both using randomization
        for tiebreakers)
"""
import sys
import os
import os.path
import argparse
import language_match


DESCRIPTION = ("Compares documents written in unknown languages to known languages.")


parser = argparse.ArgumentParser(description=DESCRIPTION,
                    formatter_class=argparse.RawDescriptionHelpFormatter)
parser.add_argument("--n-gram-max", "-n", metavar="N", type=int,
                    help="max size n-gram to store for each language")
parser.add_argument("--source", "-s", type=argparse.FileType("r"), default=sys.stdin,
                    help="file containing list of languages to process (defaults to stdin)")
parser.add_argument("--classify", "-c",
                    help="other files to classify in addition to those marked Unknown " +
                    "(may be used multiple times)")
parser.add_argument("--matches", "-m", type=int,
                    help="the number of matches to display, should be a number or 'all'")
parser.add_argument("--unknown", "-u",
                    help="the keyword designating unknown languages in input file " +
                        "(default '%(default)s')")
parser.add_argument("--data", "-d", default=None,  # Just a flag?  Make hidden files for langs?
                    help="file to use as cache for languages") #read and write to

parser.set_defaults(n_gram_max=3,
                    unknown="Unknown",
                    matches=5)


def find_langs(args):
    """ Finds all languages and associated filenames based on arguments

    Returns:
        A dict mapping language names to a list of filenames
    TODO:
        Handle an option for automatic directory traversal, ie
        --- English
        |  |-- American
        |  |-- British
        |-- French
        --- Greek
           |-- Ancient
           --- Modern
        With languages mapping to something like English/American
    """
    infile = args.source
    langs = {}
    for line in infile:
        name_and_files = line.split()
        name = name_and_files[0]
        if name not in langs:
            langs[name] = []
        for file in name_and_files[1:]:
            if os.path.isfile(file):
                langs[name].append(file)
            elif os.path.isdir(file):
                directory = file
                files = [os.path.join(directory, file) for file in os.listdir(directory)]
                langs[name] += [file for file in files if os.path.isfile(file)]
            else:
                print("File or directory {} does not exist".format(file))

    return langs



def report_matches(unknown, reference_langs, args):
    """ Matches an unknown document against known languages, prints results

    Args:
        unknown: The name of a file to classify
        reference_langs: A dict mapping language names to Language objects
    """
    matches = language_match.best_matches(unknown, reference_langs, args.n_gram_max, args.matches)
    print("Best match{} for".format("es" if args.matches != 1 else ""), repr(unknown))
    pad = max([len(name) for (name, score) in matches])
    for (name, score) in matches:
        print("\t", name.ljust(pad), "\t{:>6.2%}".format(score))



def main(args):
    """Runs the program after args have been processed"""
    reference_langs = find_langs(args) # or from cache
    unknowns = reference_langs.pop(args.unknown, [])
    reference_langs = language_match.read_languages(reference_langs, args.n_gram_max)
    for unknown in unknowns:
        report_matches(unknown, reference_langs, args)


if __name__ == "__main__":
    main(parser.parse_args())
