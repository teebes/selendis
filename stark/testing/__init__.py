#! /usr/bin/env python

import os

from fabric.operations import local
from fabric.context_managers import lcd

def get_modules_from_dir(path='.'):
    with lcd(path):
         return [
            dir for
            dir in os.listdir(path)
            if dir[-3:] == '.py'
        ]

def run():
    path = 'stark'
    for module in get_modules_from_dir(path):
        print("Testing {}...".format(module))
        with lcd(path):
            local('python -m doctest {}'.format(module))
        print("...done\n")

        

run()


