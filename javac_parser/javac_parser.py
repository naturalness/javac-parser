# Copyright (C) 2017 Joshua Charles Cambpell <joshua2@ualberta.ca>,
#                    Eddie Antonio Santos <easantos@ualberta.ca>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import os
import signal
import subprocess
import sys
import time
import unittest
from bisect import bisect_right

import msgpack
import py4j
from py4j.java_gateway import JavaGateway, launch_gateway, GatewayParameters


SOURCE_PATH = os.path.dirname(os.path.abspath(__file__))


def find_jar_path():
    "Tries to find where the lexer JAR is."
    paths = []
    jar_file = 'lex-java-1.0-SNAPSHOT-jar-with-dependencies.jar'
    # setup.py local installation
    paths.append(os.path.join(SOURCE_PATH, "share/javac-parser", jar_file))
    # pip install
    paths.append(os.path.join(sys.prefix, "share/javac-parser", jar_file))

    for path in paths:
        if os.path.exists(path):
            return path
    # Maven. The default in case the JAR must be rebuilt.
    return os.path.join(os.path.dirname(SOURCE_PATH), "target", jar_file)


JAR_PATH = find_jar_path()


class Java(object):
    @staticmethod
    def _build_jar():
        """
        Rebuilds the jar.
        """
        py4j_jar = os.path.join(sys.prefix, 'share/py4j/py4j0.10.6.jar')
        subprocess.check_call("mvn install:install-file -Dfile=" + py4j_jar +
                              " -DgroupId=py4j -DartifactId=py4j"
                              " -Dversion=0.10.6 -Dpackaging=jar"
                              " -DgeneratePom=true", shell=True)
        subprocess.check_call("mvn package", shell=True)
        assert os.path.isfile(JAR_PATH)

    def __init__(self):
        if not os.path.isfile(JAR_PATH):
            raise ImportError("Could not find the JAR file associated with "
                              "javac_parser")
        java_port = launch_gateway(jarpath=JAR_PATH,
                                   die_on_exit=True,
                                   redirect_stdout=sys.stdout,
                                   redirect_stderr=sys.stderr)
        self.gateway = JavaGateway(
            gateway_parameters=GatewayParameters(port=java_port)
        )
        self.app = self.gateway.jvm.ca.ualberta.cs.App()
        assert self.app.getNumParseErrors("") == 0

    def __enter__(self):
        return self

    def __exit__(self, *exc_info):
        self.__del__()

    def get_num_parse_errors(self, java_source):
        """
        Attempt to parse a Java source string.
        Returns the number of diagnostics generated.
        """
        return self.app.getNumParseErrors(java_source)

    def check_syntax(self, java_source):
        """
        Attempt to parse a Java source string.
        Returns a list of diagnostics generated. Each diagnostic is a
        tuple of the form:
            0. Diagnostic severity (ex. "ERROR")
            1. Error code (ex. "compiler.err.expected")
            2. Message (ex. "'{' expected')
            3. Line number
            4. Column number
            5. Start index (char position in file)
            6. End index
        """
        return [
            tuple(i) for i in self.app.checkSyntax(java_source)
        ]

    def lex_call(self, java_source):
        binary = self.app.lexFlat(java_source)
        return msgpack.unpackb(binary)

    def lex(self, java_source):
        """
        Perform lexical analysis on a Java source string.
        Returns a list of tuples of the form:
            1. Lexeme type
            2. Value (as it appears in the source file)
            3. A 2-tuple of start line, start column
            4. A 2-tuple of end line, end column
            5. A whitespace-free representation of the value
        """
        # WARNING: assumes lines not in mac format
        lpos = 0
        lines = [0]
        while True:
            lpos = java_source.find('\n', lpos) + 1
            if lpos <= 0:
                break
            lines.append(lpos)

        def convert_position(i):
            line = bisect_right(lines, i)
            col = i - lines[line - 1]
            return (line, col, i)

        def convert(lexeme):
            t, v, s, e, string = tuple(lexeme)
            string = string.decode('utf-8')
            assert ' \n\r\t' not in string
            return (
                t.decode('utf-8'),
                v.decode('utf-8'),
                convert_position(s),
                convert_position(e),
                string
            )

        return [convert(l) for l in self.lex_call(java_source)]