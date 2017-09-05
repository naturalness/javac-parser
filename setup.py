from setuptools import setup
from setuptools.command.develop import develop
from setuptools.command.install import install

import os
import sys
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
        # Note that py4j MUST be installed for this to work!
        check_call("mvn install:install-file -Dfile=" + PY4J_JAR +
                   " -DgroupId=py4j -DartifactId=py4j -Dversion=0.10.6 -Dpackaging=jar -DgeneratePom=true",
                   shell=True)
        check_call("mvn package", shell=True)
        assert os.path.isfile(JAR_PATH)
        develop.run(self)


def readme():
    import codecs
    with codecs.open('README.rst', encoding='UTF-8') as readme_file:
        return readme_file.read()


setup(
    name='javac-parser',
    version='0.1.6',
    py_modules=['javac_parser'],
    install_requires=['py4j==0.10.6'],

    author='Eddie Antonio Santos, Joshua Charles Campbell',
    author_email='easantos@ualberta.ca, joshua2@ualberta.ca',
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
    data_files=[('share/javac-parser', [JAR_PATH])],
)
