#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import re
import sys

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


def get_version(*file_paths):
    """Retrieves the version from es_synonyms/__init__.py"""
    filename = os.path.join(os.path.dirname(__file__), *file_paths)
    with open(filename) as f:
        version_file = f.read()
    version_match = re.search(r'^__version__ = \((\d+?), (\d+?), (\d+?)\)$',
                              version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError('Unable to find version string.')


version = get_version("es_synonyms", "__init__.py")


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
    os.system("git tag -a %s -m 'version %s'" % (version, version))
    os.system("git push --tags")
    sys.exit()

setup(
    name='elasticsearch-synonym-toolkit',
    version=version,
    description="""Toolkit for Elasticsearch Synonym files.""",
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
