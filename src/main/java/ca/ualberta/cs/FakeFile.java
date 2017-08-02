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
        this.contents = contents;
        this.date = new Date();
    }
    
    public URI toUri() {
        try {
            return new URI("fake://unnaturalcode/java/source/file.java");
        } catch (java.net.URISyntaxException e) {
            throw new RuntimeException(e);
        }
    }
    
    public String getName() {
        return "file.java";
    }
    
    public InputStream openInputStream() throws IOException {
        return new ByteArrayInputStream(
            contents.getBytes(StandardCharsets.UTF_8));
    }
    
    public OutputStream openOutputStream() throws IOException {
        throw new RuntimeException("Me not that kind of file.");
    }
    
    public Reader openReader(boolean ignoreEncodingErrors) throws IOException {
        return new StringReader(contents);
    }
    
    public CharSequence getCharContent(boolean ignoreEncodingErrors) 
    throws IOException {
        return contents;
    }
    
    public Writer openWriter() throws IOException {
        throw new RuntimeException("Me not that kind of file.");
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
    
    public boolean isNameCompatible(String simpleName, JavaFileObject.Kind kind) {
        return true;
    }
    
    public NestingKind getNestingKind() {
        return null;
    }
    
    public Modifier getAccessLevel() {
        return null;
    }
}
