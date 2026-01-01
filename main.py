import lexer

lex = lexer.Lexer("var a = 5;")
lex.lexer()
print(lex.tokens)