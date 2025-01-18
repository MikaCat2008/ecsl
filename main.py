from tokenizer import Tokenizer
from syntax_tree import SyntaxTree

with open("ecsl_code.ecsl") as f:
    ecsl_code = f.read()

tokenizer = Tokenizer()
tokens = tokenizer.tokenize(ecsl_code)

syntax_tree = SyntaxTree()
nodes = syntax_tree.parse(tokens)

print(nodes[None][0])
