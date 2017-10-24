from setuptools import setup
from setuptools.command.develop import develop
from setuptools.command.install import install

import codecs
import os
import sys
import shutil
import unittest
from subprocess import check_call


SOURCE_PATH = os.path.dirname(os.path.abspath(__file__))
PY4J_JAR = os.path.join(sys.prefix, 'share/py4j/py4j0.10.6.jar')
JAR_PATH = os.path.join(SOURCE_PATH, "target", "lex-java-1.0-SNAPSHOT-jar-with-dependencies.jar")


class PostDevelopCommand(develop):
    """
    Post-installation for development mode.

    Generates the JAR file required by the Python module. This should only be
    done on a development machine.
    """
    def run(self):
        # Remove target/ to FORCE the recreation of the JAR files.
        shutil.rmtree(os.path.join(SOURCE_PATH, 'target'), ignore_errors=True)
        # Note that py4j MUST be installed for this to work!
        check_call("mvn install:install-file -Dfile=" + PY4J_JAR +
                   " -DgroupId=py4j -DartifactId=py4j -Dversion=0.10.6 -Dpackaging=jar -DgeneratePom=true",
                   shell=True)
        check_call("mvn package", shell=True)
        assert os.path.isfile(JAR_PATH)
        develop.run(self)


def simple_test_suite():
    """Runs tests from javac_parser.py"""
    test_loader = unittest.TestLoader()
    return test_loader.discover(SOURCE_PATH, pattern='javac_parser.py')


def readme():
    with codecs.open('README.rst', encoding='UTF-8') as readme_file:
        return readme_file.read()


setup(
    name='javac-parser',
    version='0.2.2',
    py_modules=['javac_parser'],
    install_requires=[
        'py4j==0.10.6',
        'msgpack-python>=0.4.8'
    ],
    data_files=[('share/javac-parser', [JAR_PATH])],

    author='Joshua Charles Campbell, Eddie Antonio Santos',
    author_email='joshua2@ualberta.ca, easantos@ualberta.ca',
    description='Exposes the OpenJDK Java parser and scanner to Python',
    long_description=readme(),
    license='AGPL3+',
    url='https://github.com/naturalness/javac-parser',
    keywords='java javac parser scanner lexer tokenizer',
    classifiers=[
        'License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)'
    ],

    cmdclass={
        'develop': PostDevelopCommand,
    },
    test_suite='setup.simple_test_suite',
)
