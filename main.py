# Token types

# EOF (end-of-file) token -> indicates that no more input is left for lexical analysis.
# Lexical Analysis: Breaking input strings into tokens -> scanner, tokenizer, lexical analyzer, lexer
# Lexeme -> a sequence of characters that form a token. This is for multidigit for example. Here we implement the intger method for this reason.
# Expr method -> finds structure via the stream of tokens from get_next_token() method. Then generates results  by computing.
# Parsing -> recognizing a phrase in a stream of tokens -> Parser
# Expr -> Does both parsing and interpreting.


# Here are the guidelines that we will use to convert the grammar to source code. By following them, you can literally
# translate the grammar to a working parser:

# Each rule, R, defined in the grammar, becomes a method with the same name, and references to that rule become a method call: R().
# The body of the method follows the flow of the body of the rule using the very same guidelines.
# Alternatives (a1 | a2 | aN) become an if-elif-else statement
# An optional grouping (…)* becomes a while statement that can loop over zero or more times
# Each token reference T becomes a call to the method eat: eat(T). The way the eat method works is that it consumes the token T if it matches the
# current lookahead token, then it gets a new token from the lexer and assigns that token to the current_token internal variable.

INTEGER, PLUS, MINUS, MUL, DIV, LPAREN, RPAREN, EOF = (
    "INTEGER",
    "PLUS",
    "MINUS",
    "MUL",
    "DIV",
    "(",
    ")",
    "EOF",
)


class Token(object):
    def __init__(self, type, value):
        # token type: INTEGER, PLUS, EOF
        self.type = type
        # token value: 0,1,2,3,4,5,6,8,9, '+', '*', '-', '/' or None
        self.value = value

    def __str__(self):
        """String representation of the instance.

        Examples:
            Token(INTEGER, 3)
            Token(PLUS, '+')
        """

        return "Token({type}, {value})".format(
            type=self.type,
            value=repr(self.value),  # returns a printable representation of value
        )

    def __repr__(self):
        return self.__str__()


class Lexer(object):
    def __init__(self, text):
        # string input, e.g. "3+5"
        self.text = text
        # self.pos is in index into self.text
        self.pos = 0
        # current token instnce
        self.current_token = None
        self.current_char = self.text[self.pos]

    def error(self):
        raise Exception("Invalid character")

    def advance(self):
        """Advance the 'pos' pointer and se the current_char variable"""
        self.pos += 1
        if self.pos > len(self.text) - 1:
            self.current_char = None
        else:
            self.current_char = self.text[self.pos]

    def skip_whitespace(self):
        while self.current_char is not None and self.current_char.isspace():
            self.advance()

    def integer(self):
        """Returns a multi-digit integer consumed from the input"""
        result = ""
        while self.current_char is not None and self.current_char.isdigit():
            result += self.current_char
            self.advance()
        return int(result)

    def get_next_token(self):
        """Lexical Analyzer aka tokenizer/scanner

        Breaks up a sentence into tokens, one token at a time.

        Returns:
            Token: returns a token
        """

        while self.current_char is not None:
            if self.current_char.isspace():
                self.skip_whitespace()
                continue

            if self.current_char.isdigit():
                return Token(INTEGER, self.integer())

            if self.current_char == "+":
                self.advance()
                return Token(PLUS, "+")

            if self.current_char == "-":
                self.advance()
                return Token(MINUS, "-")

            if self.current_char == "/":
                self.advance()
                return Token(DIV, "/")

            if self.current_char == "*":
                self.advance()
                return Token(MUL, "*")

            if self.current_char == "(":
                self.advance()
                return Token(LPAREN, "(")

            if self.current_char == ")":
                self.advance()
                return Token(RPAREN, ")")

            self.error()

        return Token(EOF, None)


class Interpreter(object):
    def __init__(self, lexer):
        self.lexer = lexer
        # set current token to the first token taken from the input
        self.current_token = self.lexer.get_next_token()

    def error(self):
        raise Exception("Invalid syntax")

    def eat(self, token_type):
        # Compare the current token type with passed token
        # type and if the match then "eat" the current token
        # and assign the next token to the self.current token
        if self.current_token.type == token_type:
            self.current_token = self.lexer.get_next_token()
        else:
            self.error()

    def factor(self):
        """factor: INTEGER|LPAREN expr RPAREN"""
        token = self.current_token  # we keep a reference to the current token
        if token.type == INTEGER:
            self.eat(INTEGER)
            return token.value
        elif token.type == LPAREN:
            self.eat(LPAREN)
            result = self.expr()
            self.eat(RPAREN)
            return result

    def term(self):
        """term: factor((MUL | DIV) factor) *"""
        result = self.factor()

        while self.current_token.type in (MUL, DIV):
            token = self.current_token
            if token.type == MUL:
                self.eat(MUL)
                result = result * self.factor()
            elif token.type == DIV:
                self.eat(DIV)
                result = result / self.factor()

        return result

    def expr(self):
        """
        Arithmetic expression parser/ interpreter

        calc> 87 + 3 * (10/ 12 (3+1))

        expr: term((PLUS | MINUS) term)*
        term: factor((MUL | DIV) factor) *
        factor: INTEGER | LPAREN expr RPAREN
        """

        result = self.term()

        while self.current_token.type in (PLUS, MINUS):
            token = self.current_token
            if token.type == PLUS:
                self.eat(PLUS)
                result = result + self.term()
            elif token.type == MINUS:
                self.eat(MINUS)
                result = result - self.term()

        return result


def main():
    while True:
        try:
            _text = input("calc> ")
        except EOFError:
            break
        if not _text:
            continue
        lexer = Lexer(_text)
        interpreter = Interpreter(lexer)
        result = interpreter.expr()
        print(result)


if __name__ == "__main__":
    main()
