#! /bin/bash

if [ ! -d ve ] ; then
    virtualenv ve --no-site-packages --python=python2.7
fi

./ve/bin/python setup.py develop

./ve/bin/pip install -r REQUIREMENTS

rm -rf Stark.egg-info

source ./ve/bin/activate

./ve/bin/python stark/testing/__init__.py




