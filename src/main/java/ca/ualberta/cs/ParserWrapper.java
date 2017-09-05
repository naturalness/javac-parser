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
import javax.tools.Diagnostic;
import javax.tools.JavaFileObject;

import java.util.logging.Logger;
import java.nio.charset.StandardCharsets;
import java.io.PrintWriter;
import java.util.List;

import ca.ualberta.cs.FakeFile;
import ca.ualberta.cs.Source;

public class ParserWrapper 
{
    protected Context context;
    protected ParserFactory factory;
    private static Logger logger = Logger.getLogger("ParserWrapper");
    protected Log log;
    protected DiagnosticCollector<JavaFileObject> diagnostics;
    
    public ParserWrapper() {
        context = new Context();
        diagnostics = new DiagnosticCollector<JavaFileObject>();
        context.put(DiagnosticListener.class, diagnostics);
        new JavacFileManager(context, true, StandardCharsets.UTF_8);
        log = Log.instance(context);
        assert log.hasDiagnosticListener();
        // override the log by something like
        // context.set(Log.logKey, myLog);
        factory = ParserFactory.instance(context);
    }
    
    public Source checkSyntax(String javaSource) {
        List<Diagnostic<? extends JavaFileObject>> diags =
            parseIt(javaSource);
        Source source = new Source();
        for (Diagnostic<? extends JavaFileObject> diag : diags) {
            Object info[] = new Object[] {
                diag.getKind().name(),
                diag.getCode(),
                diag.getMessage(null),
                diag.getLineNumber(),
                diag.getColumnNumber(),
                diag.getStartPosition(),
                diag.getEndPosition()
            };
            source.add(info);
        }
        return source;
    }
    
    
    public List<Diagnostic<? extends JavaFileObject>> parseIt(String javaSource) {
        log.useSource(new FakeFile(javaSource));
        JavacParser parser = factory.newParser(javaSource, true, true, true);
        Object what = parser.parseCompilationUnit();
        return diagnostics.getDiagnostics(); 
    }
    
    public int numErrors(String javaSource) {
       return parseIt(javaSource).size();
    }

    public Source lexIt(String javaSource) {
        FakeFile fakeFile = new FakeFile(javaSource);
        log.useSource(fakeFile);
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

