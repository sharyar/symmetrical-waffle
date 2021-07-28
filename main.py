# Token types

# EOF (end-of-file) token -> indicates that no more input is left for lexical analysis.
# Lexical Analysis: Breaking input strings into tokens -> scanner, tokenizer, lexical analyzer, lexer
# Lexeme -> a sequence of characters that form a token. This is for multidigit for example. Here we implement the intger method for this reason.
# Expr method -> finds structure via the stream of tokens from get_next_token() method. Then generates results  by computing.
# Parsing -> recognizing a phrase in a stream of tokens -> Parser
# Expr -> Does both parsing and interpreting.

INTEGER, PLUS, MINUS, MUL, DIV, EOF = "INTEGER", "PLUS", "MINUS", "MUL", "DIV", "EOF"


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


class Interpreter(object):
    def __init__(self, text):
        # string input, e.g. "3+5"
        self.text = text
        # self.pos is in index into self.text
        self.pos = 0
        # current token instnce
        self.current_token = None
        self.current_char = self.text[self.pos]

    def error(self):
        raise Exception("Error parsing input")

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
        """Lexical Analyzer

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

            if self.current_char == "*":
                self.advance()
                return Token(MUL, "*")

            if self.current_char == "/":
                self.advance()
                return Token(DIV, "/")

            self.error()

        return Token(EOF, None)

    def eat(self, token_type):
        if self.current_token.type == token_type:
            self.current_token = self.get_next_token()
        else:
            self.error()

    def expr(self):
        # sets current token to the first token from the input
        self.current_token = self.get_next_token()

        # we expect first token to be an integer
        left = self.current_token
        self.eat(INTEGER)

        # we expect the current token to be a + or -
        op = self.current_token
        if op.type == PLUS:
            self.eat(PLUS)
        elif op.type == MINUS:
            self.eat(MINUS)
        elif op.type == MUL:
            self.eat(MUL)
        elif op.type == DIV:
            self.eat(DIV)
        # we expect the current token to be a integer
        right = self.current_token
        self.eat(INTEGER)
        # after the above call, the self.current_token is set to EOF token

        if op.type == PLUS:
            result = left.value + right.value
        elif op.type == MINUS:
            result = left.value - right.value
        elif op.type == MUL:
            result = left.value * right.value
        else:
            result = left.value / right.value
        return result


def main():
    while True:
        try:
            _text = input("calc> ")
        except EOFError:
            break
        if not _text:
            continue
        interpreter = Interpreter(_text)
        result = interpreter.expr()
        print(result)


if __name__ == "__main__":
    main()
