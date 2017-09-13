package ca.ualberta.cs;

import junit.framework.Test;
import junit.framework.TestCase;
import junit.framework.TestSuite;

import ca.ualberta.cs.App;

/**
 * Unit test for simple App.
 */
public class AppTest 
    extends TestCase
{
    /**
     * Create the test case
     *
     * @param testName name of the test case
     */
    public AppTest( String testName )
    {
        super( testName );
    }

    /**
     * @return the suite of tests being tested
     */
    public static Test suite()
    {
        return new TestSuite( AppTest.class );
    }

    /**
     * Rigourous Test :-)
     */
    public void testLexFlat()
    {
        App app = new App();
        byte[] b = app.lexFlat("");
        assertEquals(0x90, b[0] & 0xF0);
    }
}
