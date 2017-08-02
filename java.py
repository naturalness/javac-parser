from py4j.java_gateway import JavaGateway

class Java(object):
    def __init__(self):
        from py4j.java_gateway import JavaGateway
        self.gateway = JavaGateway()
        
    def get_num_parse_errors(self, java_source):
        return self.gateway.entry_point.getNumParseErrors(java_source)
    
    
import unittest
class TestJava(unittest.TestCase):
    def test_parse_ok(self):
        java = Java()
        self.assertEqual(java.get_num_parse_errors(''), 0)
        
    def test_parse_ok_class(self):
        java = Java()
        s = """
            package ca.ualberta.cs;
            
            import java.util.logging.Logger;
            
            public class Bogus {
                public int a = 1;
            }
        """
        self.assertEqual(java.get_num_parse_errors(s), 0)

    def test_parse_one_error(self):
        java = Java()
        s = """
            package ca.ualberta.cs;
            
            import java.util.logging.Logger;
            
            public class Bogus {
                public int a = 1;
                public int b = ;
            }
        """
        self.assertEqual(java.get_num_parse_errors(s), 1)
    
    def test_parse_two_error(self):
        java = Java()
        s = """
            package ca.ualberta.cs;
            
            import java.util.logging.Logger;
            
            public class Bogus {
                public int a = 1;
                public int b = ;
            
        """
        self.assertEqual(java.get_num_parse_errors(s), 2)
    
if __name__ == '__main__':
    unittest.main()
