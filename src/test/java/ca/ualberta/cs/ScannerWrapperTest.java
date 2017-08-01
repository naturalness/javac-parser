package ca.ualberta.cs;

import junit.framework.Test;
import junit.framework.TestCase;
import junit.framework.TestSuite;

import ca.ualberta.cs.ScannerWrapper;

/**
 * Unit tests for scanner wrapper.
 */
public class ScannerWrapperTest 
    extends TestCase
{
    /**
     * Create the test case
     *
     * @param testName name of the test case
     */
    public ScannerWrapperTest( String testName )
    {
        super( testName );
    }

    /**
     * @return the suite of tests being tested
     */
    public static Test suite()
    {
        return new TestSuite( ScannerWrapperTest.class );
    }

    public void testInstantiate()
    {
        ScannerWrapper sw = new ScannerWrapper();
    }

    public void testLex()
    {
        ScannerWrapper sw = new ScannerWrapper();
        sw.lexIt("a = 1 + 2");
    }
}
