from setuptools import setup
from distutils.spawn import find_executable

import os
import sys
import subprocess


# Generate the JAR file.
# Hacky, but this works.
SOURCE_PATH = os.path.dirname(os.path.abspath(__file__))
PY4J_JAR = os.path.join(sys.prefix, 'share/py4j/py4j0.10.6.jar')
JAR_PATH = os.path.join(SOURCE_PATH,
                        "target",
                        "lex-java-1.0-SNAPSHOT-jar-with-dependencies.jar")
if find_executable('mvn'):
      subprocess.check_call("mvn install:install-file -Dfile=" + PY4J_JAR + " -DgroupId=py4j -DartifactId=py4j -Dversion=0.10.6 -Dpackaging=jar -DgeneratePom=true", shell=True)
      subprocess.check_call("mvn package", shell=True)
assert os.path.isfile(JAR_PATH)


setup(name='javac-parser',
      version='0.1.3',
      py_modules=['javac_parser'],
      data_files=[('share/javac-parser', [JAR_PATH])],
      install_requires=['py4j==0.10.6'],

      author='Eddie Antonio Santos, Joshua Charles Campbell',
      author_email='easantos@ualberta.ca, joshua2@ualberta.ca',
      description='Exposes the OpenJDK Java parser and scanner to Python',
      license='AGPL3+',
      keywords='java javac parser scanner lexer tokenizer',
      classifiers=[
            'License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)'
      ]
)
