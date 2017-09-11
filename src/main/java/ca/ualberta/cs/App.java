package ca.ualberta.cs;

import ca.ualberta.cs.ParserWrapper;
import ca.ualberta.cs.Source;

import py4j.GatewayServer;

import org.msgpack.jackson.dataformat.MessagePackFactory;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.core.JsonProcessingException;

public class App 
{
    public ObjectMapper objectMapper = new ObjectMapper(new MessagePackFactory());

    public int getNumParseErrors(String javaSource) {
        return (new ParserWrapper()).numErrors(javaSource);
    }
    
    public Source lex(String javaSource) {
        return (new ParserWrapper()).lexIt(javaSource);
    }
    
    public Source checkSyntax(String javaSource) {
        return (new ParserWrapper()).checkSyntax(javaSource);
    }

    public byte[] lexFlat(String javaSource) {
         Source r = (new ParserWrapper()).lexIt(javaSource);
         try {
            return objectMapper.writeValueAsBytes(r);
        } catch (JsonProcessingException e) {
            throw new RuntimeException(e);
        }
    }

    public static void main( String[] args )
    {
        GatewayServer gatewayServer = new GatewayServer(new App());
        gatewayServer.start();
//         System.out.println("Java Lexer/Parser Server Started");
    }
}

