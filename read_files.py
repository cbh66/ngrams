
import os
import os.path
import glob
import braceexpand

def expand_file_expression(name):
    """ Expands Unix-style wildcards in nearly the same way the shell would

    Handles home directory shortcuts, brace expansion, environment variables,
    and wildcard characters.
    Args:
        name: A string representing a filename to potentially expand
    Returns:
        A list of file names matching the pattern.  The list may be empty.
        All names represent existing files (though could potentially be
        broken symlinks).
    """
    try:
        names = braceexpand.braceexpand(name)
    except braceexpand.UnbalancedBracesError:
        names =[name]
    names = [os.path.expanduser(os.path.expandvars(elem)) for elem in names]
    results = []
    for elem in names:
        results.extend(glob.glob(elem))
    return results


def filter_files(lst):
    """ Returns a list of all files specified.

    In particular, reports an error if a file does not exist, and finds files
    within any directories that are specified.
    Args:
        lst: A list of supposed file and directory names
    Returns:
        A list of valid file names.
    """
    results = []
    for elem in lst:
        for name in expand_file_expression(elem):
            if os.path.isfile(name):
                results.append(name)
            elif os.path.isdir(name):
                directory = name
                files = [os.path.join(directory, file) for file in os.listdir(directory)]
                results += [file for file in files if os.path.isfile(file)]
            # else not possible; file must exist
    return results