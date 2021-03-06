from typing import List, Tuple, Union


# severity, error code, message, line no (1-indexed), column no (0-indexed),
# start index (UTF-16 index in the file), end index (UTF-16 index in the file)
Diagnostic = Tuple[str, str, str, int, int, int]
# lexeme type, value, start (1-indexed line no, 0-indexed column),
# end (1-indexed line no, 0-indexed column no),
# a whitespace free version of the value.
Token = Tuple[str, str, Tuple[int, int], Tuple[int, int], str]


class Java:
    def check_syntax(self, java_source: Union[str, bytes]) -> List[Diagnostic]: ...
    def get_num_parse_errors(self, java_source: Union[str, bytes]) -> int: ...
    def lex(self, java_source: str) -> List[Token]: ...
