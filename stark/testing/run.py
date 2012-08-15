#! /usr/bin/env python
import os
import unittest
from unittest import TestLoader

from fabric.operations import local
from fabric.context_managers import lcd, hide

def get_modules_from_dir(path='.'):
    with lcd(path):
         return [
            dir for
            dir in os.listdir(path)
            if dir[-3:] == '.py'
        ]

def run_doctests():
    path = 'stark'
    for module in get_modules_from_dir(path):
        print("\tTesting {}...".format(module))
        with lcd(path):
            with hide('running'):
                local('python -m doctest {}'.format(module))

if __name__ == "__main__":
    print "\nRunning doc tests..."
    run_doctests()

    print "\nRunning unit tests..."
    loader = unittest.TestLoader()
    tests = loader.discover('.')
    import stark
    import doctest
    tests.addTests(doctest.DocTestSuite(stark))
    unittest.runner.TextTestRunner().run(tests)

    print "\n==============\nDone\n\n"
