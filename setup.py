#!/usr/bin/env python

from distutils.core import setup

setup(name='taco',
      version='0.0.0',
      description='Taco Python module',
      author='Graham Bell',
      author_email='graham.s.bell@gmail.com',
      url='http://github.com/grahambell/taco-python',
      package_dir={'': 'lib'},
      packages=['taco'],
      scripts=['scripts/taco-python'],
      classifiers=['License :: OSI Approved :: '
                       'GNU General Public License v3 (GPLv3)',
                   'Development Status :: 3 - Alpha'],
)
