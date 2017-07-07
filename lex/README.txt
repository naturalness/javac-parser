maven package

java -cp /home/joshua/unnaturalcode/java/lex-java/target/lex-java-1.0-SNAPSHOT-jar-with-dependencies.jar ca.ualberta.cs.App

python -m jcc --include target/lex-java-1.0-SNAPSHOT-jar-with-dependencies.jar ca.ualberta.cs.ScannerWrapper --python unnaturalcode_java_lex --build --install

unnaturalcode_java_lex.initVM()
sw = unnaturalcode_java_lex.ScannerWrapper()
sw.lexIt("c = a + b;")
