"""
Helper functions for the views that require extra logic like parsing
directories or running tests.
"""

import os
import unittest


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
            modules += ["{}{}{}".format(root,os.sep,f) for f in files if f.startswith("test_")]

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
