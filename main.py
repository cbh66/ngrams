
import sys
import os
import os.path
import argparse
import language_match


DESCRIPTION = ("Compares documents written in unknown languages to known languages.  " +
"An input file must be provided with known languages, with lines of the form" +
"""
    English english1.txt english2.txt
    French  french/
    English english3.txt
    Unknown tbd.txt
""" +
"Where each line has a language name and the name of 1 or more files written in that language, " +
"or the name of a directory containing files in that language.  " +
"If the language name is the 'Unknown' keyword, the language will be classified.")

# Eventually: add option for traversing directory structure
# Also: allow wildcards and such.  See expanduser() and expandvars()
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
parser.add_argument("--data", "-d", default=None,
                    help="file to use as cache for languages") #read and write to

parser.set_defaults(n_gram_max=3,
                    unknown="Unknown",
                    matches=5)

# finds filenames associated with languages, returns dict of langs to filename list
def find_langs(args):
    # If not directory traversal option....
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
    matches = language_match.best_matches(unknown, reference_langs, args.n_gram_max, args.matches)
    print("Best match{} for".format("es" if args.matches != 1 else ""), repr(unknown))
    pad = max([len(name) for (name, score) in matches])
    for (name, score) in matches:
        print("\t", name.ljust(pad), "\t{:>6.2%}".format(score))



def main(args):
    reference_langs = find_langs(args) # or from cache
    unknowns = reference_langs.pop(args.unknown, [])
    reference_langs = language_match.read_languages(reference_langs, args.n_gram_max)
    for unknown in unknowns:
        report_matches(unknown, reference_langs, args)


if __name__ == "__main__":
    main(parser.parse_args())
