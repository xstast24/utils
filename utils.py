import glob
import os
import re
import sys


def count_dir_lines(dir_path, recursive=False, file_filters=None):
    """
    Count lines in all files in given directory. May also search recursively in subdirs etc.
    Results can be filtered, e.g. only certain file types. Note: If no filters given, searching may fail,
    because some file types (e.g. archives) can't be read properly as UTF-8 symbols (searching newlines).
    :param dir_path: path to the directory
    :param recursive: recursively count also all files in subdirs, subsubdirs, ..., etc.
    :param file_filters: Count only files matching any of these filters. Filter are regular exp. patterns.
        Example: [r'\w*.py', r'\w*.sh'] to match all *.py and *.sh files
    :return number of lines in all files in given directory (based on given params and filters),
        return -1 if directory not found
    """
    if os.path.exists(dir_path):
        lines = 0
        # list all files/dirs, filter them if any filters given
        for file in glob.glob(os.path.join(dir_path, '**'), recursive=recursive):
            if os.path.isfile(file):
                if file_filters:
                    # count only lines in files matching given filters
                    for name_filter in file_filters:
                        if re.match(name_filter, os.path.basename(file)):
                            lines += count_file_lines(file)
                            break  # in case more filters would match one file
                else:
                    # no filters given, count lines in all found files
                    lines += count_file_lines(file)
        return lines
    else:
        # given path does not exist
        print("Error: Given path not found: {}".format(dir_path), file=sys.stderr)
        return -1


def count_file_lines(file_path):
    """
    Count lines in given file. Ignores empty last line (only one).
    :param file_path: path to the file
    :return number of lines in the file, return -1 if file not found
    """
    if os.path.isfile(file_path):
        i = 0
        with open(file_path, 'r') as f:
            for i, l in enumerate(f):
                pass
        return i+1
    else:
        print("Error: Not a file: {}".format(file_path))
        return -1


""" EXAMPLE USAGE """
if __name__ == '__main__':
    line_count = count_dir_lines(os.getcwd(), recursive=False, file_filters=[r'\w*.py'])
    print("Number of lines in this directory: {}".format(line_count))
    line_count = count_file_lines('/This/File/Does/not.exist')
    print("Number of lines in non-existing file: {}".format(line_count))
