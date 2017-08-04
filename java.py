import logging
logger = logging.getLogger(__name__)
error = logger.error
warn = logger.warn
info = logger.info
debug = logger.debug

import os
import subprocess
import time
import signal
from bisect import bisect_right

import py4j
from py4j.java_gateway import JavaGateway

SOURCE_PATH = os.path.dirname(os.path.abspath(__file__))
JAR_PATH = os.path.join(SOURCE_PATH, 
                        "target",
                        "lex-java-1.0-SNAPSHOT-jar-with-dependencies.jar")

class Java(object):
    def __init__(self):
        java_cmd = subprocess.check_output("which java",
                                             shell=True).rstrip()
        try:
            self.gateway = JavaGateway()
            self.gateway.entry_point.getNumParseErrors("")
        except py4j.protocol.Py4JNetworkError:
            pass
        else:
            raise RuntimeError("Old java server still running")
        if os.path.isfile(JAR_PATH):
            pass
        else:
            subprocess.check_call("mvn install:install-file -Dfile=${VIRTUAL_ENV}/share/py4j/py4j0.10.6.jar -DgroupId=py4j -DartifactId=py4j -Dversion=0.10.6 -Dpackaging=jar -DgeneratePom=true", shell=True)
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
        tries = 100
        while True:
            try:
                time.sleep(0.1)
                self.gateway = JavaGateway()
                self.gateway.entry_point.getNumParseErrors("")
            except py4j.protocol.Py4JNetworkError:
                tries -= 1
                if tries > 0:
                    continue
                else:
                    raise
            else:
                break
    
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
        return self.gateway.entry_point.getNumParseErrors(java_source)
    
    @staticmethod
    def fix_extra_quotes(lexeme):
        l = tuple(lexeme)
    
    def lex(self, java_source):
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
        error(lexed)
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
        error(repr(lexed))
        self.assertEqual(lexed[3][0], 'ERROR')



    def tearDown(self):
        del self.java
    
if __name__ == '__main__':
    unittest.main()
