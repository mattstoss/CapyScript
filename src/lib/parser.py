from lib import ast
from lib.token import TokenKind


class Parser:
    def __init__(self, tokens):
        self._tokens = tokens
        self._idx = 0
        self._nodes = []

    def parse(self):
        if len(self._nodes) == 0:
            while not self._is_end():
                new_node = self._decl()
                self._nodes.append(new_node)
        return self._nodes

    def _decl(self):
        current = self._current()
        if current.kind == TokenKind.Let:
            return self._var_decl()
        elif current.kind == TokenKind.Func:
            return self._func_decl()
        elif current.kind == TokenKind.Class:
            return self._class_decl()
        else:
            return self._stmt()

    def _var_decl(self):
        self._match(TokenKind.Let)
        name = self._match(TokenKind.Identifier).string
        self._match(TokenKind.Equal)
        expr = self._expr()
        return ast.VarDecl(name, expr)

    def _func_decl(self):
        self._match(TokenKind.Func)
        name = self._match(TokenKind.Identifier).string
        self._match(TokenKind.OpenParen)
        params = self._params()
        self._match(TokenKind.CloseParen)
        block = self._block()
        return ast.FuncDecl(name, params, block)

    def _class_decl(self):
        self._match(TokenKind.Class)
        name = self._match(TokenKind.Identifier).string
        self._match(TokenKind.OpenBracket)
        body = []
        while not self._is_match(TokenKind.CloseBracket):
            body.append(self._func_decl())
        self._match(TokenKind.CloseBracket)
        return ast.ClassDecl(name, body)

    def _params(self):
        params = []
        while not self._is_match(TokenKind.CloseParen):
            name = self._match(TokenKind.Identifier).string
            new_param = ast.Param(name)
            params.append(new_param)
            if not self._is_match(TokenKind.CloseParen):
                self._match(TokenKind.Comma)
        return params

    def _args(self):
        args = []
        while not self._is_match(TokenKind.CloseParen):
            expr = self._expr()
            new_arg = ast.Arg(expr)
            args.append(new_arg)
            if not self._is_match(TokenKind.CloseParen):
                self._match(TokenKind.Comma)
        return args

    def _stmt(self):
        current = self._current()
        if current.kind == TokenKind.Print:
            return self._print_stmt()
        elif current.kind == TokenKind.Return:
            return self._return_stmt()
        else:
            return self._expr_stmt()

    def _print_stmt(self):
        self._match(TokenKind.Print)
        expr = self._expr()
        return ast.Print(expr)

    def _return_stmt(self):
        self._match(TokenKind.Return)
        expr = self._expr()
        return ast.Return(expr)

    def _expr_stmt(self):
        return self._expr()

    def _expr(self):
        return self._assignment()

    def _assignment(self):
        expr = self._call()

        if self._is_match(TokenKind.Equal):
            if isinstance(expr, ast.Identifier) or isinstance(expr, ast.GetProperty):
                self._match(TokenKind.Equal)
                value = self._assignment()
                return ast.Assignment(expr, value)
            else:
                raise ValueError(f"parser: can't assignment to {type(expr)}")

        return expr

    def _call(self):
        expr = self._primary()

        while True:
            if self._is_match(TokenKind.OpenParen):
                self._match(TokenKind.OpenParen)
                args = self._args()
                self._match(TokenKind.CloseParen)
                expr = ast.Call(expr, args)
            elif self._is_match(TokenKind.Dot):
                self._match(TokenKind.Dot)
                name = self._match(TokenKind.Identifier).string
                expr = ast.GetProperty(expr, name)
            else:
                break

        return expr

    def _block(self):
        self._match(TokenKind.OpenBracket)
        nodes = []
        while not self._is_match(TokenKind.CloseBracket):
            nodes.append(self._decl())
        self._match(TokenKind.CloseBracket)
        return ast.Block(nodes)

    def _primary(self):
        current = self._require_current()
        self._advance()
        if current.kind == TokenKind.StringLiteral:
            return ast.String(current.string)
        elif current.kind == TokenKind.Identifier:
            return ast.Identifier(current.string)
        else:
            raise ValueError(f"parser: unexpected token: {current}")

    def _is_match(self, token_kind, lookahead=0):
        idx = self._idx + lookahead
        if idx < len(self._tokens):
            return self._tokens[idx].kind == token_kind
        return False

    def _match(self, token_kind):
        current = self._require_current()
        if current.kind != token_kind:
            raise ValueError(
                f"parser: unexpected token [want: {token_kind}, got: {current.kind}]"
            )
        self._advance()
        return current

    def _advance(self):
        self._idx += 1

    def _require_current(self):
        if self._is_end():
            raise ValueError("parser: unexpected end of input")
        return self._current()

    def _current(self):
        return self._tokens[self._idx]

    def _is_end(self):
        return self._idx >= len(self._tokens)
