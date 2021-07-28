# Token types

# EOF (end-of-file) token -> indicates that no more input is left for lexical analysis.
# Lexical Analysis: Breaking input strings into tokens -> scanner, tokenizer, lexical analyzer, lexer

INTEGER, PLUS, EOF = "INTEGER", "PLUS", "EOF"


class Token(object):
    def __init__(self, type, value):
        # token type: INTEGER, PLUS, EOF
        self.type = type
        # token value: 0,1,2,3,4,5,6,8,9, '+', or None
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

    def error(self):
        raise Exception("Error parsing input")

    def get_next_token(self):
        """Lexical Analyzer

        Breaks up a sentence into tokens, one token at a time.

        Returns:
            Token: returns a token
        """

        text = self.text

        if self.pos > len(text) - 1:
            return Token(EOF, None)

        current_char = text[self.pos]

        if current_char.isdigit():
            token = Token(INTEGER, int(current_char))
            self.pos += 1
            return token

        if current_char == "+":
            token = Token(PLUS, current_char)
            self.pos += 1
            return token

        self.error()

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

        # we expect the current token to be a +
        op = self.current_token
        self.eat(PLUS)

        right = self.current_token
        self.eat(INTEGER)
        # after the above call, the self.current_token is set to EOF token

        result = left.value + right.value
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
