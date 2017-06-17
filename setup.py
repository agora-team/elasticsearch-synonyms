#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import re
import sys

from os import path
from setuptools import setup

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as fp:
  long_description = fp.read()

with open(path.join(here, 'es_synonyms', '__init__.py'), encoding='utf-8') as fp:
  rex = r'^__version__ = \((\d+?), (\d+?), (\d+?)\)$'
  vtp = re.search(rex, fp.read(), re.M).groups()
  __version__ = '.'.join(vtp)


if sys.argv[-1] == 'publish':
    try:
      import wheel
      print("Wheel version: ", wheel.__version__)
    except ImportError:
      print('Wheel library missing. Please run "pip install wheel"')
      sys.exit()
    os.system('python setup.py sdist upload')
    os.system('python setup.py bdist_wheel upload')
    sys.exit()

if sys.argv[-1] == 'tag':
    print("Tagging the version on git:")
    os.system("git tag -a %s -m 'version %s'" % (__version__, __version__))
    os.system("git push --tags")
    sys.exit()

setup(
  name='elasticsearch-synonym-toolkit',
  version=__version__,
  description="""Toolkit for Elasticsearch Synonym files.""",
  long_description=long_description,
  author='Prashant Sinha',
  author_email='prashant+git@noop.pw',
  url='https://github.com/prashnts/dj-elasticsearch-flex',
  packages=[
    'es_synonyms',
  ],
  include_package_data=True,
  install_requires=['hues'],
  entry_points={
    'console_scripts': ['es-synlint=es_synonyms.synlint:cli'],
  },
  license="MIT",
  zip_safe=False,
  keywords='elasticsearch-synonym-toolkit',
  classifiers=[
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: MIT License',
    'Natural Language :: English',
    'Programming Language :: Python :: 2',
    'Programming Language :: Python :: 2.7',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.2',
    'Programming Language :: Python :: 3.3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
  ],
)
