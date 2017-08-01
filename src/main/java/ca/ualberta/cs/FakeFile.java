package ca.ualberta.cs;

import com.sun.tools.javac.util.Context;
import javax.tools.JavaFileObject;

import java.util.logging.Logger;
import java.util.Date;
import java.io.IOException;
import java.io.InputStream;
import java.io.ByteArrayInputStream;
import java.io.OutputStream;
import java.io.Reader;
import java.io.StringReader;
import java.io.Writer;
import java.net.URI;
import java.nio.charset.StandardCharsets;
import javax.lang.model.element.NestingKind;
import javax.lang.model.element.Modifier;


public class FakeFile implements JavaFileObject {
    protected String contents;
    protected Date date;
    
    public FakeFile(String contents) {
        self.contents = contents;
        self.date = Date();
    }
    
    public URI toUri() {
        return URI("fake://unnaturalcode/java/source/file.java");
    }
    
    public String getName() {
        return "file.java";
    }
    
    public InputStream openInputStream() throws IOException {
        return new ByteArrayInputStream(
            exampleString.getBytes(StandardCharsets.UTF_8));
    }
    
    public OutputStream openOutputStream() throws IOException {
        return null;
    }
    
    public Reader openReader(boolean ignoreEncodingErrors) throws IOException {
        return new StringReader(contents);
    }
    
    public CharSequence getCharContent(boolean ignoreEncodingErrors) 
    throws IOException {
        return contents;
    }
    
    public Writer openWriter() throws IOException {
        return null;
    }
    
    public long getLastModified() {
        return date.getTime();
    }
    
    public boolean delete() {
        return true;
    }
    
    public JavaFileObject.Kind getKind() {
        return JavaFileObject.Kind.SOURCE;
    }
    
    boolean isNameCompatible(String simpleName, JavaFileObject.Kind kind) {
        return true;
    }
    
    NestingKind getNestingKind() {
        return null;
    }
    
    Modifier getAccessLevel() {
        return null;
    }
}
