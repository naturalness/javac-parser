from setuptools import setup, find_packages
from setuptools.command.develop import develop

import codecs
import os
import sys
import shutil
import unittest
from subprocess import check_call


SOURCE_PATH = os.path.dirname(os.path.abspath(__file__))
TEST_PATH = os.path.join(SOURCE_PATH, 'tests')
PY4J_JAR = os.path.join(sys.prefix, 'share/py4j/py4j0.10.6.jar')
JAR_PATH = os.path.join(SOURCE_PATH, "target", "lex-java-1.0-SNAPSHOT-jar-with-dependencies.jar")


class PostDevelopCommand(develop):
    """
    Post-installation for development mode.

    This must occur AFTER py4j is installed.

    Generates the JAR file required by the Python module. This should only be
    done on a development machine.
    """
    def run(self):
        # Remove target/ to FORCE the recreation of the JAR files.
        shutil.rmtree(os.path.join(SOURCE_PATH, 'target'), ignore_errors=True)
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


setup(
    name='javac-parser',
    version='0.2.2',
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
    include_package_data=True,
    data_files=[('share/javac-parser', [JAR_PATH])],

    license='AGPL3+',
    keywords='java javac parser scanner lexer tokenizer',
    classifiers=[
        'License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)'
    ],

    cmdclass={
        'develop': PostDevelopCommand,
    },
    test_suite='setup.simple_test_suite',
)
