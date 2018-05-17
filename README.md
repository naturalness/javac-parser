javac parser
============


![PyPI](https://img.shields.io/pypi/v/javac-parser.svg) ![PyPI - License](https://img.shields.io/pypi/l/javac-parser.svg) [![Build Status](https://travis-ci.org/naturalness/javac-parser.svg?branch=master)](https://travis-ci.org/naturalness/javac-parser)

Use OpenJDK's Java parser ("javac") in Python!

Install
-------

    pip install javac-parser

Usage
-----

First, instantiate the server:

```python
import javac_parser
java = javac_parser.Java()
```

Count the number of syntax errors:

```python
>>> java.get_num_parse_errors('class Hello {')
1
>>> java.get_num_parse_errors('class Hello { }')
0
```

Get a list of diagnostics for each syntax error:

```python
>>> java.check_syntax('class Hello {')
[('ERROR', 'compiler.err.premature.eof', 'reached end of file while parsing', 1, 14, 13, 13)]'
>>> java.check_syntax('class Hello { }')
[]
```

Lex (tokenize) Java source code, even if it does not compile:

```python
>>> java.lex('class Hello {')
[('CLASS', 'class', (1, 0), (1, 5), 'class'), ('IDENTIFIER', 'Hello', (1, 6), (1, 11), 'Hello'), ('LBRACE', '{', (1, 12), (1, 13), '{'), ('EOF', '', (1, 13), (1, 13), 'token.end-of-input')]
```

See the docstrings in ``javac_parser.py`` or type `pydoc javac_parser` for more details!


Copying
-------

Copyright (C) 2017, 2018  Joshua Charles Campbell and Eddie Antonio Santos

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
