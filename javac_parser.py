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

import logging
logger = logging.getLogger(__name__)
error = logger.error
warn = logger.warn
info = logger.info
debug = logger.debug

import sys
import os
import subprocess
import time
import signal
from bisect import bisect_right

import py4j
from py4j.java_gateway import JavaGateway

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
    # Maven.
    return os.path.join(SOURCE_PATH, "target", jar_file)

JAR_PATH = find_jar_path()


class Java(object):
    def check_alive(self):
        if not hasattr(self, 'gateway'):
            self.gateway = JavaGateway()
        try:
            assert self.gateway.entry_point.getNumParseErrors("") == 0
        except py4j.protocol.Py4JNetworkError:
            return False
        else:
            return True
    
    def __init__(self):
        java_cmd = subprocess.check_output("which java",
                                             shell=True).rstrip()
        if self.check_alive():
            warn("Old java server still running... re-using it.")
            warn("Java server will not be killed on exit.")
            warn("Please kill it manually.")
            return
        if os.path.isfile(JAR_PATH):
            pass
        else:
            py4j_jar = os.path.join(sys.prefix, 'share/py4j/py4j0.10.6.jar')
            subprocess.check_call("mvn install:install-file -Dfile=" + py4j_jar + " -DgroupId=py4j -DartifactId=py4j -Dversion=0.10.6 -Dpackaging=jar -DgeneratePom=true", shell=True)
            subprocess.check_call("mvn package", shell=True)
            assert os.path.isfile(JAR_PATH)
        self.java_server = subprocess.Popen(
            [
                java_cmd,
                "-jar",
                JAR_PATH
            ],
            preexec_fn=os.setsid
        )
        timeout = 10 # seconds
        tries = 1000
        while not self.check_alive():
            time.sleep(timeout/tries)
            tries -= 1
            if tries > 0:
                continue
            else:
                error("Couldn't connect to java server...")
                self.gateway.entry_point.getNumParseErrors("")

    def __del__(self):
        #error("killing %i" % self.java_server.pid)
        if hasattr(self, 'gateway'):
            self.gateway.shutdown()
            self.gateway.close()
            del self.gateway
        if hasattr(self, 'java_server'):
            os.killpg(os.getpgid(self.java_server.pid), signal.SIGTERM)
            self.java_server.wait()

    def get_num_parse_errors(self, java_source):
        """
        Attempt to parse a Java source string.
        Returns the number of diagnostics generated.
        """
        return self.gateway.entry_point.getNumParseErrors(java_source)
    
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
            tuple(i) for i in self.gateway.entry_point.checkSyntax(java_source)
            ]

    @staticmethod
    def fix_extra_quotes(lexeme):
        l = tuple(lexeme)

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
            lpos = java_source.find('\n', lpos)+1
            if lpos <= 0:
                break
            lines.append(lpos)

        def convert_position(i):
            line = bisect_right(lines, i)
            col = i-lines[line-1]
            return (line, col)

        def convert(lexeme):
            t, v, s, e, string = tuple(lexeme)
            assert not (' \n\r\t' in string)
            return (
                t,
                v,
                convert_position(s),
                convert_position(e),
                string
                )

        return [convert(l) for l in self.gateway.entry_point.lex(java_source)]

import unittest
class TestJava(unittest.TestCase):
    def setUp(self):
        self.java = Java()

    def test_parse_ok(self):
        self.assertEqual(self.java.get_num_parse_errors(''), 0)

    def test_parse_ok_class(self):
        s = """
            package ca.ualberta.cs;

            import java.util.logging.Logger;

            public class Bogus {
                public int a = 1;
            }
        """
        self.assertEqual(self.java.get_num_parse_errors(s), 0)

    def test_parse_one_error(self):
        s = """
            package ca.ualberta.cs;

            import java.util.logging.Logger;

            public class Bogus {
                public int a = 1;
                public int b = ;
            }
        """
        self.assertEqual(self.java.get_num_parse_errors(s), 1)

    def test_parse_two_error(self):
        s = """
            package ca.ualberta.cs;

            import java.util.logging.Logger;

            public class Bogus {
                public int a = 1;
                public int b = ;

        """
        self.assertEqual(self.java.get_num_parse_errors(s), 2)

    def test_lex(self):
        s = """
package ca.ualberta.cs;

import java.util.logging.Logger;

public class Bogus {
    public int a = 1;
    public String s = "hamburgers";
}
"""
        lexed = self.java.lex(s)
        #error(lexed)
        self.assertEqual(len(lexed), 34)
        self.assertEqual(lexed[0][0], 'PACKAGE')
        self.assertEqual(lexed[0][1], 'package')
        self.assertEqual(lexed[0][2][0], 2)
        self.assertEqual(lexed[0][2][1], 0)
        self.assertEqual(lexed[0][3][0], 2)
        self.assertEqual(lexed[0][3][1], len('package'))
        self.assertEqual(lexed[0][4], 'package')
        self.assertEqual(lexed[2][1], '.')

    def test_lex_error(self):
        s = "String x = \\"
        lexed = self.java.lex(s)
        #error(repr(lexed))
        self.assertEqual(lexed[3][0], 'ERROR')

    def test_check_syntax_ok(self):
        s = """
package ca.ualberta.cs;

import java.util.logging.Logger;

public class Bogus {
    public int a = 1;
    public String s = "hamburgers";
}
"""
        errs = self.java.check_syntax(s)
        #error(repr(errs))
        self.assertEqual(len(errs), 0)

    def test_check_syntax_eof(self):
        s = """
package ca.ualberta.cs;

import java.util.logging.Logger;

public class Bogus {
    public int a = 1;
    public String s = "hamburgers";

"""
        errs = self.java.check_syntax(s)
        #error(repr(errs))
        self.assertEqual(len(errs), 1)

    def test_check_syntax_ob(self):
        s = """
package ca.ualberta.cs;

import java.util.logging.Logger;

public class Bogus 
    public int a = 1;
    public String s = "hamburgers";
}
"""
        errs = self.java.check_syntax(s)
        error(repr(errs))
        self.assertEqual(len(errs), 1)

    def tearDown(self):
        del self.java

if __name__ == '__main__':
    unittest.main()
