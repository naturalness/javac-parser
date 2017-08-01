package ca.ualberta.cs;

import junit.framework.Test;
import junit.framework.TestCase;
import junit.framework.TestSuite;

import ca.ualberta.cs.ParserWrapper;

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
}
