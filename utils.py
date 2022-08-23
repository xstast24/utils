import glob
import os
import re
import sys


def count_lines(path, recursive=True, filters=None):
    """
    Count lines in given file/directory. May also search recursively in subdirs etc.
    Can be filtered, e.g. only certain file types. Note: If no filters given, searching directories may fail,
    because they may contain some file types (e.g. archives) that can't be read properly as UTF-8 symbols (searching newlines).
    Note 2: Doesn't count 1 last empty line.
    :param path: target file or directory
    :param recursive: recursively count lines also in all files in subdirs, subsubdirs, ..., etc.
    :param filters: count line only in files matching any of these filters. Filters are regex patterns.
        Example: [r'\w*.py', r'\w*.sh'] to match *.py and *.sh files
    :return: number of lines in given file or directory
    """
    if os.path.isdir(path):
        return count_dir_lines(path, recursive, filters)
    elif os.path.isfile(path):
        return count_file_lines(path)
    else:
        raise FileNotFoundError("Path {} does not exist!".format(path))


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


def _wait_for_variable(condition: Any, expected_value: Any, end_time: float, period: float):
    """
    Same as 'wait_for', but only supports variable conditions (non-callable). The 'end_time' [timestamp] is the time when waiting is ended.
    :return: 1) True if condition passed under given timeout, False otherwise, 2) latest value of the condition
    """
    latest_value = condition
    while time.time() < end_time:
        if latest_value == expected_value:
            return True, latest_value

        time.sleep(period)
        latest_value = condition

    return False, latest_value


def _wait_for_callable(condition: Callable, args: list, kwargs: dict, expected_value: Any, end_time: float, period: float):
    """
    Same as 'wait_for', but only supports callable conditions. The 'end_time' [timestamp] is the time when waiting is ended.
    :return: 1) True if condition passed under given timeout, False otherwise, 2) latest value of the condition
    """
    latest_value = condition(*args, **kwargs)
    while time.time() < end_time:
        if (latest_value) == expected_value:
            return True, latest_value
        time.sleep(period)
        latest_value = condition(*args, **kwargs)

    return False, latest_value


def wait_for(condition: Any, args: Optional[list] = None, kwargs: Optional[dict] = None, expected_value: Any = True,
             timeout: float = 10, period: float = 1, raise_exc: bool = False) -> bool:
    """
    Wait for any condition (variable/callable) to have the expected value. Condition is checked periodically until the timeout is reached.
    :param condition: variable or callable object that is checked
    :param args: args for callable condition (all in a single list)
    :param kwargs: kwargs for callable condition (all in a single dict)
    :param expected_value: desired value of the condition
    :param timeout: [seconds] max wait time
    :param period: [seconds] interval to periodically check condition
    :param raise_exc: if waiting is not successful -> raise TimeoutError exception (instead of returning "False")
    :return: True if condition passed under given timeout, False otherwise
    Examples: wait_for(lambda: os.path.exists(path))  # wait for file existence (using lambda), return False if not created
              wait_for(math.is_close, args=[my_var, 42], kwargs={'abs_tol': 0.01}, expected_value=True, timeout=5, period=0.2)
              wait_for(os.path.exists, args=[path], raise_exc=True)  # wait for file existence (using a callable with args),
                                                                     raise TimeoutError if file hasn't been created in time
    """
    end_time = time.time() + timeout
    if callable(condition):
        args = args if args else []
        kwargs = kwargs if kwargs else {}
        result, last_value = _wait_for_callable(condition, args, kwargs, expected_value, end_time, period)
    else:
        result, last_value = _wait_for_variable(condition, expected_value, end_time, period)

    if result is False and raise_exc:
        raise TimeoutError(f'Condition not fulfilled in time:\nExpected value: {expected_value}\nActual value: {last_value}')

    return result


""" EXAMPLE USAGE """
if __name__ == '__main__':
    line_count = count_dir_lines(os.getcwd(), recursive=False, file_filters=[r'\w*.py'])
    print("Number of lines in this directory: {}".format(line_count))
    line_count = count_file_lines('/This/File/Does/not.exist')
    print("Number of lines in non-existing file: {}".format(line_count))
