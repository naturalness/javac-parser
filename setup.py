#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Note: To use the 'upload' functionality of this file, you must:
#   $ pip install twine

import codecs
import os
import sys
from shutil import rmtree

from setuptools import Command, find_packages, setup
from setuptools.command.develop import develop

NAME = 'javac_parser'
DESCRIPTION = 'Exposes the OpenJDK Java parser and scanner to Python'


# Various paths that this script needs to check.
HERE = os.path.dirname(os.path.abspath(__file__))
TEST_PATH = os.path.join(HERE, 'tests')
JAR_NAME = "lex-java-1.0-SNAPSHOT-jar-with-dependencies.jar"
DISTRIBUTABLE_JAR_PATH = os.path.join(HERE, os.path.join(NAME, JAR_NAME))


class UploadCommand(Command):
    """Support setup.py upload."""

    description = 'Build and publish the package.'
    user_options = []

    @staticmethod
    def status(s):
        """Prints things in bold."""
        print('\033[1m{0}\033[0m'.format(s))

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        try:
            self.status('Removing previous builds…')
            rmtree(os.path.join(HERE, 'dist'))
        except OSError:
            pass

        assert os.path.isfile(DISTRIBUTABLE_JAR_PATH)
        self.status('Building Source and Wheel (universal) distribution…')
        os.system('{0} setup.py sdist bdist_wheel --universal'.format(sys.executable))

        self.status('Uploading the package to PyPi via Twine…')
        os.system('twine upload dist/*')

        self.status('Pushing git tags…')
        os.system('git tag v{0}'.format(version()))
        os.system('git push --tags')

        sys.exit()


class PostDevelopCommand(develop):
    """
    Post-installation for development mode.

    This must occur AFTER py4j is installed.

    Generates the JAR file required by the Python module. This should only be
    done on a development machine.
    """
    def run(self):
        # Remove target/ to FORCE the recreation of the JAR files.
        rmtree(os.path.join(HERE, 'target'), ignore_errors=True)
        from javac_parser import Java
        Java._build_jar()
        assert os.path.isfile(DISTRIBUTABLE_JAR_PATH)
        develop.run(self)


def simple_test_suite():
    """Runs tests from tests/"""
    import unittest
    test_loader = unittest.TestLoader()
    return test_loader.discover(TEST_PATH)


def readme():
    with codecs.open('README.rst', encoding='UTF-8') as readme_file:
        return readme_file.read()


def version():
    """
    Load the package's __version__.py module as a dictionary.
    Derived from: https://github.com/kennethreitz/setup.py/blob/59cfa99b99d87bf2cb2e9176c6dfcacafb532023/setup.py#L41-L46
    """
    about = {}
    with open(os.path.join(HERE, NAME, '__version__.py')) as f:
        exec(f.read(), about)
    return about['__version__']


setup(
    name=NAME,
    version=version(),
    description=DESCRIPTION,
    author='Joshua Charles Campbell, Eddie Antonio Santos',
    author_email='joshua2@ualberta.ca, easantos@ualberta.ca',
    long_description=readme(),
    url='https://github.com/naturalness/javac-parser',
    packages=find_packages(exclude=('tests',)),

    install_requires=[
        'py4j==0.10.6',
        'msgpack-python>=0.4.8'
    ],
    package_data={
        NAME: [JAR_NAME]
    },
    test_suite='setup.simple_test_suite',

    license='AGPL3+',
    keywords='java javac parser scanner lexer tokenizer',
    classifiers=[
        'License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)'
    ],

    cmdclass={
        'develop': PostDevelopCommand,
        'upload': UploadCommand,
    },
)
