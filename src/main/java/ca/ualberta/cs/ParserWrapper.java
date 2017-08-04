package ca.ualberta.cs;

import com.sun.tools.javac.util.Context;
import com.sun.tools.javac.util.Log;
import com.sun.tools.javac.util.AbstractLog;
import com.sun.tools.javac.parser.ParserFactory;
import com.sun.tools.javac.parser.JavacParser;
import com.sun.tools.javac.file.JavacFileManager;
import com.sun.tools.javac.parser.ScannerFactory;
import com.sun.tools.javac.parser.Scanner;
import static com.sun.tools.javac.parser.Tokens.*;

import javax.tools.DiagnosticCollector;
import javax.tools.DiagnosticListener;

import java.util.logging.Logger;
import java.nio.charset.StandardCharsets;
import java.io.PrintWriter;

import ca.ualberta.cs.FakeFile;
import ca.ualberta.cs.Source;

public class ParserWrapper 
{
    protected Context context;
    protected ParserFactory factory;
    private static Logger logger = Logger.getLogger("ParserWrapper");
    protected Log log;
    protected DiagnosticCollector<FakeFile> diagnostics;
    
    public ParserWrapper() {
        context = new Context();
        diagnostics = new DiagnosticCollector<FakeFile>();
        context.put(DiagnosticListener.class, diagnostics);
        new JavacFileManager(context, true, StandardCharsets.UTF_8);
        log = Log.instance(context);
        assert log.hasDiagnosticListener();
        // override the log by something like
        // context.set(Log.logKey, myLog);
        factory = ParserFactory.instance(context);
    }
    
    public void parseIt(String javaSource) {
        JavacParser parser = factory.newParser(javaSource, true, true, true);
        log.useSource(new FakeFile(javaSource));
        Object what = parser.parseCompilationUnit();
    }
    
    public int numErrors(String javaSource) {
        JavacParser parser = factory.newParser(javaSource, true, true, true);
        log.useSource(new FakeFile(javaSource));
        Object what = parser.parseCompilationUnit();
//         logger.info(what.toString());
//         for (Object x : diagnostics.getDiagnostics()) {
//             logger.info(x.toString());
//         }
       return diagnostics.getDiagnostics().size();
    }

    public Source lexIt(String javaSource) {
        log.useSource(new FakeFile(javaSource));
        ScannerFactory factory;
        factory = ScannerFactory.instance(context);
        Scanner scanner = factory.newScanner(javaSource, true);
        Token prevToken = null;
        Source source = new Source();
        do  {
            scanner.nextToken();
            prevToken = scanner.token();
            String value;
            String str;
            try {
                str = prevToken.name().toString();
                value = str;
            } catch (UnsupportedOperationException e) {
                str = prevToken.kind.toString();
                if (str.charAt(0) == '\'') {
                    str = str.substring(1, str.length() - 1);
                }
                try {
                    value = prevToken.stringVal();
                } catch (UnsupportedOperationException ee) {
                    value = str;
                }
            }
            Object lexeme[] = new Object[] {
                prevToken.kind.name(), 
                javaSource.substring(prevToken.pos, prevToken.endPos),
                prevToken.pos, 
                prevToken.endPos, 
                str
            };
            source.add(lexeme);
        } while (prevToken.kind != TokenKind.EOF);
        return source;
    }
}

