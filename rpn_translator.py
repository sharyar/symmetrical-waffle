from spi import Lexer, NodeVisitor, Parser

# Lexer -> Produces tokens from input
# Parser -> Takes tokens and determines expressions
# Interpreter -> Converts expressions into values


class RPN_Interpreter(NodeVisitor):
    def __init__(self, parser):
        self.tree = tree

    def visit_BinOp(self, node):
        left_val = self.visit(node.left)
        right_val = self.visit(node.right)
        return "{left} {right} {op}".format(
            left=left_val, right=right_val, op=node.op.value
        )

    def visit_Num(self, node):
        return node.value

    def translate(self):
        return self.visit(self.tree)


if __name__ == "__main__":
    while True:
        text = input("trm > ")
        lexer = Lexer(text)
        parser = Parser(lexer)
        tree = parser.parse()
        translator = RPN_Interpreter(tree)
        translation = translator.translate()
        print(translation)
