#!/usr/bin/env python

from distutils.core import setup

with open('README.rst') as f:
    long_description = f.read()

setup(
    name='taco',
    version='0.1.0',
    description='Taco module for Python',
    long_description=long_description,
    author='Graham Bell',
    author_email='graham.s.bell@gmail.com',
    url='http://github.com/grahambell/taco-python',
    package_dir={'': 'lib'},
    packages=['taco'],
    scripts=['scripts/taco-python'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
