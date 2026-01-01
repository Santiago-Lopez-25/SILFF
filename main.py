import lexer, parser, interpreter
import sys

def main():
    if len(sys.argv) > 1:
        source_file = sys.argv[1]
    else:
        source_file = "source.silff"
    
    try:
        with open(source_file, "r") as f:
            code = f.read()
            lex = lexer.Lexer(code)
            lex.lexer()
            tokens = lex.tokens
            ast = parser.Parser(tokens)
            ast.parse()
            ast = ast.ast
            evaluator = interpreter.Interpreter(ast)
            evaluator.evaluate()
    except FileNotFoundError:
        print(f"error: file '{source_file}' not found")

if __name__ == "__main__": 
    main()        