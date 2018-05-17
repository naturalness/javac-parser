from setuptools import setup, find_packages
from setuptools.command.develop import develop

import codecs
import os
import sys
import shutil
import unittest
from subprocess import check_call

NAME = 'javac_parser'

HERE = os.path.dirname(os.path.abspath(__file__))
TEST_PATH = os.path.join(HERE, 'tests')
RELATIVE_JAR_PATH = os.path.join("target", "lex-java-1.0-SNAPSHOT-jar-with-dependencies.jar")
JAR_PATH = os.path.join(HERE, RELATIVE_JAR_PATH)


class PostDevelopCommand(develop):
    """
    Post-installation for development mode.

    This must occur AFTER py4j is installed.

    Generates the JAR file required by the Python module. This should only be
    done on a development machine.
    """
    def run(self):
        # Remove target/ to FORCE the recreation of the JAR files.
        shutil.rmtree(os.path.join(HERE, 'target'), ignore_errors=True)
        from javac_parser import Java
        Java._build_jar()
        assert os.path.isfile(JAR_PATH)
        develop.run(self)


def simple_test_suite():
    """Runs tests from tests/"""
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
    description='Exposes the OpenJDK Java parser and scanner to Python',
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
        NAME: [RELATIVE_JAR_PATH]
    },
    test_suite='setup.simple_test_suite',

    license='AGPL3+',
    keywords='java javac parser scanner lexer tokenizer',
    classifiers=[
        'License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)'
    ],

    cmdclass={
        'develop': PostDevelopCommand,
    },
)
