VVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVV
if using pyenv: 
export VIRTUAL_ENV="$(pyenv prefix)"

py4j instructions:

mvn install:install-file -Dfile=${VIRTUAL_ENV}/share/py4j/py4j0.10.6.jar -DgroupId=py4j -DartifactId=py4j -Dversion=0.10.6 -Dpackaging=jar -DgeneratePom=true

mvn package

java -jar target/lex-java-1.0-SNAPSHOT-jar-with-dependencies.jar
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

JCC instructions:

maven package

java -cp /home/joshua/unnaturalcode/java/lex-java/target/lex-java-1.0-SNAPSHOT-jar-with-dependencies.jar ca.ualberta.cs.App

python -m jcc --include target/lex-java-1.0-SNAPSHOT-jar-with-dependencies.jar ca.ualberta.cs.ScannerWrapper --python unnaturalcode_java_lex --build --install

unnaturalcode_java_lex.initVM()
sw = unnaturalcode_java_lex.ScannerWrapper()
sw.lexIt("c = a + b;")
