#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

# Copyright (C) 2017, 2018 Hazel Campbell and Eddie Antonio Santos
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

import unittest

from javac_parser import Java


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
        self.assertEqual(len(errs), 1)

    def test_check_syntax_illegal(self):
        s = """#
"""
        self.java.lex(s)
        errs = self.java.check_syntax(s)
        self.assertEqual(len(errs), 2)

    def test_check_syntax_huge(self):
        # Generate a MASSIVE syntactically-valid Java file.
        # Create a few thousand copies of this method enough changes to make
        # it valid.
        def sub(i):
            t = """
    public void test##() {
        ParserWrapper sw = new ParserWrapper();
        assertEquals(1, sw.numErrors(
            "package ca.ualberta.cs;\\n"
            + "import java.util.logging.Logger;\\n"
            + "public class ParserWrapper {\\n"
            + "  public int a = ##;\\n"
            + "}\\n"
            + "##:\\n"
        ));}
"""
            return t.replace("##", str(i))
        s = """
package ca.ualberta.cs;

import java.util.logging.Logger;

public class Bogus {
%s
}
""" % ("\n".join([sub(i) for i in range(0, 4700)]))
        tokens = list(self.java.lex(s))
        # There will be AT LEAST the amount of tokens as amount of lines.
        assert len(tokens) >= 4700

        errs = self.java.check_syntax(s)
        self.assertEqual(len(errs), 0)

    def tearDown(self):
        del self.java
