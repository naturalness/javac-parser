package ca.ualberta.cs;

import junit.framework.Test;
import junit.framework.TestCase;
import junit.framework.TestSuite;
import junit.framework.Assert.*;

import ca.ualberta.cs.ParserWrapper;
import ca.ualberta.cs.Source;

/**
 * Unit tests for scanner wrapper.
 */
public class ParserWrapperTest
    extends TestCase
{
    /**
     * Create the test case
     *
     * @param testName name of the test case
     */
    public ParserWrapperTest( String testName )
    {
        super( testName );
    }

    /**
     * @return the suite of tests being tested
     */
    public static Test suite()
    {
        return new TestSuite( ParserWrapperTest.class );
    }

    public void testInstantiate()
    {
        ParserWrapper sw = new ParserWrapper();
    }

    public void testParse()
    {
        ParserWrapper sw = new ParserWrapper();
        sw.parseIt(
            "package ca.ualberta.cs;\n"
            + "import java.util.logging.Logger;\n"
            + "public class ParserWrapper {\n"
            + "}\n"
        );
    }
    public void testBadParse()
    {
        ParserWrapper sw = new ParserWrapper();
        sw.parseIt(
            "package ca.ualberta.cs;\n"
            + "import java.util.logging.Logger;\n"
            + ":alksdjflasdfjk"
            + "public class ParserWrapper {\n"
            + "}\n"
        );
    }
    public void testNumErrors()
    {
        ParserWrapper sw = new ParserWrapper();
        assertEquals(0, sw.numErrors(
            "package ca.ualberta.cs;\n"
            + "import java.util.logging.Logger;\n"
            + "public class ParserWrapper {\n"
            + "  public int a = 1;\n"
            + "}\n"
        ));
    }
    public void testOneErrors()
    {
        ParserWrapper sw = new ParserWrapper();
        assertEquals(1, sw.numErrors(
            "package ca.ualberta.cs;\n"
            + "import java.util.logging.Logger;\n"
            + "public class ParserWrapper {\n"
            + "  public int a = 1;\n"
            + "}\n"
            + "akljsdhflasjdfa:\n"
        ));
    }
    public void testOneErrorsB()
    {
        ParserWrapper sw = new ParserWrapper();
        assertEquals(1, sw.numErrors(
            "package ca.ualberta.cs;\n"
            + "import java.util.logging.Logger;\n"
            + "public class ParserWrapper {\n"
            + "  public int a = 1;\n"
            + "akljsdhflasjdfa:\n"
            + "}\n"
        ));
    }

    public void testLex()
    {
        ParserWrapper sw = new ParserWrapper();
        assertEquals(6, sw.lexIt("a = 1 + 2").size());
    }


    /**
     * Test ability to cope with The Java® Language Specification §3.5.
     *
     * https://docs.oracle.com/javase/specs/jls/se8/html/jls-3.html#jls-3.5
     */
    public void testUnicodeEscapes()
    {
        ParserWrapper sw = new ParserWrapper();
        String program = "public class \\u0042 {}";

        assertEquals(0, (new ParserWrapper()).numErrors(program));
        Source src = sw.lexIt(program);
        /* Regression: lexing the Unicode escape in the class name should
         * return "B".
         * Discussion: https://github.com/naturalness/javac-parser/issues/1 */
        assertEquals("B", src.get(2)[1]);
    }

    /**
     * Test ability to cope with The Java® Language Specification §3.5.
     *
     * https://docs.oracle.com/javase/specs/jls/se8/html/jls-3.html#jls-3.5
     */
    public void testInputElementSub()
    {
        ParserWrapper sw = new ParserWrapper();
        assertEquals(5, sw.lexIt("class A{}\u001a").size());
    }
}
