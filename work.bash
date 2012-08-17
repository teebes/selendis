#! /bin/bash

if [ ! -d ve ] ; then
    virtualenv ve --no-site-packages --python=python2.7
fi

source ./ve/bin/activate

make


