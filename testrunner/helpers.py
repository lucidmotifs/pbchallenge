"""
Helper functions for the views that require extra logic like parsing
directories or running tests.
"""

import os, subprocess

# the test directory relative to where our web app runs from
# this would be an absolute directory were we not using django tests
# and if this app didn't need to be portable (while it has not config)
TESTS_DIR = 'testrunner/tests/'
# used for unittest execution
TESTS_DIR_ABS = '/Users/paulcooper/Documents/GitHub/pbchallenge/testrunner/tests'
TESTING_COMMAND = ['./manage.py', 'test']

def execute_test_django(test_path):
    """
    Execute a given test in a way that is compatible with Django,
    which is different because django must set-up its own DB and
    configure its settings.
    """
    # remove the leading './' if exists
    if test_path.startswith('./') or test_path.startswith('.\\'):
        # remove the first 2 chars
        test_path = test_path[2:]

    # remove .py at the end, if its found
    if test_path.endswith('.py'):
        test_path = test_path[:-3]

    # attached the TEST_DIR to the path
    test_path = "{}{}".format(TESTS_DIR, test_path)

    # turn the path into a python module string
    test_module = test_path.replace(os.sep, '.')

    # add test module to the command
    command = TESTING_COMMAND + [test_module,]
    #command.append('2>')
    #command.append('output.txt')

    # start a subprocess and store output
    # the env var passed is so that the output from subprocess
    # is not truncated
    p = subprocess.run(command, \
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding="utf-8")
    #result,err = p.communicate()

    # actual test result output is always in stderr, stdout is just info
    return p.stderr


def get_test_modules(root_dir):
    """
    Starting at `root` crawl the filesystem looking for:
        - directories containing files starting with test_
        - any file beginning with test_
    """
    modules = list()
    dir = {}
    if os.path.isdir(root_dir):
        # store the current directory
        cwd = os.getcwd()
        # switch to the directory
        os.chdir(root_dir)
        # traverse the given directory
        for root, dir, files in os.walk('.'):
            # loads all test modules into a list
            modules += ["{}{}{}".format(root,os.sep,f) \
                for f in files if f.startswith("test_") \
                               and not f.endswith(".pyc")]

        # return to the original dir
        os.chdir(cwd)

    return modules


def create_hierarchy(files):
    """
    Builds a nested dict that contains a representation of the
    filesystem hierarchy of the given list of files.
    """
    if len(files) is 0:
        print('emtpy files list')
        return None

    fs = dict()
    # lose the initial slashes, if any.
    start = files[0].rfind(os.sep) + 1

    for f in files:
        # generate a list of folders
        folders = f[start:].split(os.sep)
        # create a dict for each entry
        subdir = dict.fromkeys(folders)

        # copy the dict
        subdir_c = subdir.copy()
        try:
            # go from last to second entry and fold down the dicts
            for i in reversed(folders[1:]):
                d = { i: subdir_c[i] }
                # retrieve the parent key
                p_key = folders[folders.index(i)-1]
                subdir_c[p_key] = d

                del subdir_c[i]
        except Exception as e:
            # catching all and printing for debug reasons
            # would bubble up error in prod.
            print(e)

        item = list(subdir_c.items())[0]

        # create a new entry for a folder or add to an exisiting one
        if item[0] in fs.keys():
            fs[item[0]].update(item[1])
        else:
            fs.update(list(subdir_c.items()))

    return fs


def reduce_hierarchy(a_dict, root="root"):
    """
    Takes a nested dictionary representation of a filesystem and
    reduces it so that each file is grouped within a folders 'files'
    key, rather than being loose and having a 'None' value.

    This simplifies displaying/running the tests.
    """
    if len(a_dict) is 0:
        return None

    reduced = list()
    # add the folder name and the initial value
    reduced.append(root)
    for key, value in a_dict.items():
        # if the value is a dict, recursively reduce to list
        if isinstance(value, dict):
            reduced.append(reduce_hierarchy(value, key))
        else:
            reduced.append(key)

    return reduced




# temp code
#m = get_test_modules('/Users/paulcooper/Documents/GitHub/pbchallenge/testrunner/tests')
#d = create_hierarchy(m)
#l = reduce_hierarchy(d)
#print(modules_to_db(m))
