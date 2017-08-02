package ca.ualberta.cs;

import com.sun.tools.javac.util.Context;
import com.sun.tools.javac.parser.ScannerFactory;
import com.sun.tools.javac.parser.Scanner;
import static com.sun.tools.javac.parser.Tokens.*;

import java.util.logging.Logger;



public class ScannerWrapper 
{

    protected Context context;
    protected ScannerFactory factory;
    private static Logger log = Logger.getLogger("ScannerWrapper");
    public ScannerWrapper() {
        context = new Context();
        factory = ScannerFactory.instance(context);
    }
    
    public void lexIt(String javaSource) {
        Scanner scanner = factory.newScanner(javaSource, true);
        Token prevToken = null;
        while (prevToken == null || prevToken.kind != TokenKind.EOF) {
            scanner.nextToken();
            prevToken = scanner.token();
            log.info( prevToken.kind.toString() );
        }
    }
}

