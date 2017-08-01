package ca.ualberta.cs;

import com.sun.tools.javac.util.Context;
import com.sun.tools.javac.util.Log;
import com.sun.tools.javac.util.AbstractLog;
import com.sun.tools.javac.parser.ParserFactory;
import com.sun.tools.javac.parser.JavacParser;
import com.sun.tools.javac.file.JavacFileManager;

import java.util.logging.Logger;
import java.nio.charset.StandardCharsets;



public class ParserWrapper 
{
    protected Context context;
    protected ParserFactory factory;
    private static Logger log = Logger.getLogger("ParserWrapper");
    public ParserWrapper() {
        context = new Context();
        new JavacFileManager(context, true, StandardCharsets.UTF_8);
        Source.instance(context);
        Log log = Log.instance(context);
        log.useSource();
        // override the log by something like
        // context.set(Log.logKey, myLog);
        factory = ParserFactory.instance(context);
    }
    
    public void parseIt(String javaSource) {
        JavacParser parser = factory.newParser(javaSource, true, true, true);
        parser.parseCompilationUnit();
    }
}

