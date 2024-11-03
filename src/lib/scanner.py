from lib.token import Token, TokenKind
from frozendict import frozendict

_keywords_dict = frozendict(
    {
        "print": TokenKind.Print,
        "let": TokenKind.Let,
        "fn": TokenKind.Func,
        "return": TokenKind.Return,
    }
)

_symbols_dict = frozendict(
    {
        "(": TokenKind.OpenParen,
        ")": TokenKind.CloseParen,
        "{": TokenKind.OpenBracket,
        "}": TokenKind.CloseBracket,
        ",": TokenKind.Comma,
        "=": TokenKind.Equal,
    },
)


def _compute_symbols_which_match_prefix(prefix):
    return {key for key in _symbols_dict.keys() if key.startswith(prefix)}


class Scanner:
    def __init__(self, input):
        self._input = input
        self._idx = 0
        self._tokens = []

    def scan(self):
        if len(self._tokens) == 0:
            while self._has_current():
                self._scan_starting_from_current()
        return self._tokens

    def _scan_starting_from_current(self):
        char = self._current()
        if char.isspace():
            self._consume_whitespace()
        elif char.isalpha():
            self._consume_string()
        elif char == '"':
            self._consume_string_literal()
        elif self._is_single_line_comment():
            self._consume_single_line_comment()
        elif self._is_symbol():
            self._consume_symbol()
        else:
            raise ValueError(f"scanner: unrecognized character '{char}'")

    def _consume_whitespace(self):
        while self._try_current().isspace():
            self._advance()

    def _consume_string(self):
        new_string = ""
        while self._try_current().isalnum() or self._try_current() == "_":
            new_string += self._current()
            self._advance()

        if new_string in _keywords_dict:
            token_kind = _keywords_dict[new_string]
            self._add_token(token_kind)
        else:
            self._add_token(TokenKind.Identifier, literal=new_string)

    def _consume_string_literal(self):
        assert self._current() == '"'
        self._advance()

        new_string = ""
        while self._try_current() not in ["\n", '"']:
            new_string += self._current()
            self._advance()

        if self._current() != '"':
            raise ValueError("scanner: unterminated string literal '{new_string}'")
        self._advance()

        self._add_token(TokenKind.StringLiteral, literal=new_string)

    def _is_symbol(self):
        current = self._current()
        matching_keys = _compute_symbols_which_match_prefix(current)
        return len(matching_keys) > 0

    def _consume_symbol(self):
        longest_match = ""
        matching_keys = _compute_symbols_which_match_prefix(self._current())
        while self._try_current() in matching_keys:
            longest_match = self._current()
            self._advance()
        token_kind = _symbols_dict[longest_match]
        self._add_token(token_kind)

    def _is_single_line_comment(self):
        return self._current() == "/" and self._try_next() == "/"

    def _consume_single_line_comment(self):
        while self._try_current() != "\n":
            self._advance()

    def _add_token(self, kind, literal=""):
        new_token = Token(kind, literal)
        self._tokens.append(new_token)

    def _current(self):
        return self._input[self._idx]

    def _has_current(self):
        return self._idx < len(self._input)

    def _try_current(self):
        if self._has_current():
            return self._current()
        return ""

    def _next(self):
        return self._input[self._idx + 1]

    def _has_next(self):
        return self._idx + 1 < len(self._input)

    def _try_next(self):
        if self._has_next():
            return self._next()
        return ""

    def _advance(self):
        self._idx += 1
