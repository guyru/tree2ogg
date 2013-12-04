#! /usr/bin/python

import os
from setuptools import setup

# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name='tree2ogg',
    version='0.1',
    # TODO: add descrition
    url='http://www.guyrutenberg.com/',
    author='Guy Rutenberg',
    author_email='guyrutenberg@gmail.com',
    license = 'GPLv2+',
    scripts=['tree2ogg'],
    long_description=read('README.rst'),
    package_data={'radiopy': ['data/radiopy.default']},

    # TODO: add classifiers
    # classifiers = [
    #     'Environment :: Console',
    #     'Intended Audience :: End Users/Desktop'
    #     'License :: OSI Approved :: GNU General Public License v2 or later (GPLv2+)'
    #     ],
)

