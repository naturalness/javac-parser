from setuptools import setup

setup(name='javac-parser',
      version='0.1.0',
      py_modules=['javac_parser'],
      install_requires=['py4j>=0.10.6'],

      author='Eddie Antonio Santos, Joshua Charles Campbell',
      author_email='easantos@ualberta.ca, joshua2@ualberta.ca',
      description='Exposes the OpenJDK Java parser and scanner to Python',
      license='AGPL3+',
      keywords='java javac parser scanner lexer tokenizer',
      classifiers=[
            'License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)'
      ]
)
