package ca.ualberta.cs;

/**
 * Hello world!
 *
 */
 
import ca.ualberta.cs.ScannerWrapper;

public class App 
{
    public static void main( String[] args )
    {
        ScannerWrapper sw = new ScannerWrapper();
        sw.lexIt("a = 1 + 2");
    }
}

