package ca.ualberta.cs;

import ca.ualberta.cs.ParserWrapper;
import ca.ualberta.cs.Source;

import py4j.GatewayServer;

public class App 
{
    public int getNumParseErrors(String javaSource) {
        return (new ParserWrapper()).numErrors(javaSource);
    }
    
    public Source lex(String javaSource) {
        return (new ParserWrapper()).lexIt(javaSource);
    }

    public static void main( String[] args )
    {
        GatewayServer gatewayServer = new GatewayServer(new App());
        gatewayServer.start();
//         System.out.println("Java Lexer/Parser Server Started");
    }
}

