package ca.ualberta.cs;

import com.sun.tools.javac.util.Context;
import com.sun.tools.javac.util.Log;
import com.sun.tools.javac.util.AbstractLog;
import com.sun.tools.javac.parser.ParserFactory;
import com.sun.tools.javac.parser.JavacParser;
import com.sun.tools.javac.file.JavacFileManager;

import java.util.logging.Logger;
import java.nio.charset.StandardCharsets;

import ca.ualberta.cs.FakeFile;

public class ParserWrapper 
{
    protected Context context;
    protected ParserFactory factory;
    private static Logger logger = Logger.getLogger("ParserWrapper");
    protected Log log;
    public ParserWrapper() {
        context = new Context();
        new JavacFileManager(context, true, StandardCharsets.UTF_8);
        log = Log.instance(context);
        // override the log by something like
        // context.set(Log.logKey, myLog);
        factory = ParserFactory.instance(context);
    }
    
    public void parseIt(String javaSource) {
        JavacParser parser = factory.newParser(javaSource, true, true, true);
        log.useSource(new FakeFile(javaSource));
        parser.parseCompilationUnit();
    }
}

