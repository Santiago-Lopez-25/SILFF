from lexer import Tk, Tktype

DEBUG = not True

class AstNode: pass

# value
class IntegerNode:
    def __init__(self,value):
        self.value = value
    def __repr__(self):
        return f"Integer {self.value}"
class FloatNode:
    def __init__(self,value):
        self.value = value
    def __repr__(self):
        return f'Float {self.value}'
class StringNode:
    def __init__(self,value):
        self.value = value
    def __repr__(self):
        return f'String {self.value}'
class BoolNode: 
    def __init__(self,value):
        self.value = value
    def __repr__(self):
        return f'Bool {self.value}'

class BlockNode(AstNode): # stats
    def __init__(self,stats):
        self.stats = stats
    def __repr__(self):
        return f'Block {self.stats}\n'

class NothingNode(AstNode): 
    def __init__(self):
        pass
    def __repr__(self):
        return f'NOTHING'

class IdNode(AstNode): # id
    def __init__(self,id):
        self.id = id
    def __repr__(self):
        return f'Id {self.id}'

class VarDecl(AstNode): # name, value
    def __init__(self,name,value):
        self.name = name
        self.value = value
    def __repr__(self):
        return f'VarDecl {self.name} >> {self.value}\n'
    
class IfNode(AstNode): # condition, block, eblock
    def __init__(self,condition,block,eblock):
        self.condition = condition
        self.block = block
        self.eblock = eblock
    def __repr__(self):
        return f'If {self.condition}\n{{{self.block}}}\n{{{self.eblock}}}\n'

class BinOpNode(AstNode): # left, op, rigth
    def __init__(self,left,op,rigth):
        self.left = left
        self.op = op
        self.rigth = rigth
    def __repr__(self):
        return f'BinOp {self.left} {self.op} {self.rigth}\n'

class UnaryNode(AstNode): # lex, value
    def __init__(self,lex,value):
        self.type = lex
        self.value = value
    def __repr__(self):
        return f'Unary {self.type} {self.value}\n'

class PrintNode(AstNode):
    def __init__(self,expr):
        self.expr = expr
    def __repr__(self):
        return f'Print {self.expr}'

class ReadNode(AstNode):
    def __init__(self,msg):
        self.msg = msg
    def __repr__(self):
        return f'Read {self.msg}'

class Parser:
    def __init__(self,tokens):
        self.tokens = tokens
        self.pos = 0
        self.ast = []
    def __repr__(self):
        s = ""
        for node in self.ast:
            s+=f'{node}'
        return s

    def peek(self)->Tk | None:
        if self.pos < len(self.tokens):
            return self.tokens[self.pos]
    def advance(self):
        self.pos += 1
    def eat(self,type:Tktype):
        if self.peek().type == type:
            var = self.peek()
            self.advance()
            return var
        else:
            print(f"expected {type}, found {self.peek().type}")
            exit(2)
    def parse_decl(self):
        print(f'curr: {self.peek()} from parse_decl') if DEBUG else None
        match self.peek().type:
            case Tktype.Var:
                return self.parse_var()
            case Tktype.If:
                return self.parse_if()
            case Tktype.Id:
                return self.parse_primary()
            case Tktype.Print:
                return self.parse_print()
            case Tktype.Read:
                return self.parse_read()
            case Tktype.Nothing:
                self.advance()
                return NothingNode()
            case _:
                return self.parse_expr()
    def parse_var(self):
        print(f'curr: {self.peek()} from parse_var') if DEBUG else None
        self.eat(Tktype.Var)
        name = self.eat(Tktype.Id).span
        self.eat(Tktype.Assing)
        expr = self.parse_expr()
        self.eat(Tktype.Semicolon)
        return VarDecl(name,expr)
    def parse_if(self):
        print(f'curr: {self.peek()} from parse_if') if DEBUG else None
        self.eat(Tktype.If)
        cond = self.parse_expr()
        block = self.parse_block()
        eblock = None
        if self.peek().type == Tktype.Else:
            self.eat(Tktype.Else)
            if self.peek().type == Tktype.Lbrace:
                eblock = self.parse_block()
            else:
                eblock = self.parse_decl()
        return IfNode(cond,block,eblock)
    def parse_block(self):
        print(f'curr: {self.peek()} from parse_block') if DEBUG else None
        self.eat(Tktype.Lbrace)
        stats = []
        while not self.peek().type in [Tktype.Rbrace,Tktype.Eof]:
            stats.append(self.parse_decl())
        self.eat(Tktype.Rbrace)
        return BlockNode(stats)
    def parse_print(self):
        self.eat(Tktype.Print)
        expr = self.parse_expr()
        self.eat(Tktype.Semicolon)
        return PrintNode(expr)
    def parse_read(self):
        self.eat(Tktype.Read)
        msg = self.parse_expr()
        return ReadNode(msg)
    def parse_expr(self):
        print(f'curr: {self.peek()} from parse_expr') if DEBUG else None
        left = self.parse_eq()
        while self.peek().type in [Tktype.Plus,Tktype.Minus]:
            op = self.peek().type
            self.advance()
            right = self.parse_eq()
            left = BinOpNode(left,op,right)
        return left
    def parse_eq(self):
        print(f'curr: {self.peek()} from parse_eq') if DEBUG else None
        left = self.parse_cmp()
        while self.peek().type in [Tktype.Eq,Tktype.Ne]:
            op = self.peek().type
            self.advance()
            right = self.parse_cmp()
            left = BinOpNode(left,op,right)
        return left
    def parse_cmp(self):
        left = self.parse_factor()
        print(f"curr: {self.peek()} from parse_cmp!") if DEBUG else None
        while self.peek().type in [Tktype.Gt,Tktype.Lt,Tktype.Le,Tktype.Ge]:
            op = self.peek().type
            self.advance()
            right = self.parse_factor()
            left = BinOpNode(left,op,right)
        return left
    def parse_factor(self):
        print(f'curr: {self.peek()} from parse_factor') if DEBUG else None
        node = self.parse_unary()
        while self.peek().type in [Tktype.Star,Tktype.Slash]:
            op = self.peek().type
            self.eat(op)
            node = BinOpNode(node,op,self.parse_unary())  
        return node
    def parse_unary(self):
        print(f'curr: {self.peek()} from parse_unary') if DEBUG else None
        node = None
        while self.peek().type in [Tktype.Minus]:
            lex = self.peek().span
            self.eat(self.peek().type) 
            r = self.parse_unary()
            node = UnaryNode(lex,r)
        if node is None:
            return self.parse_primary()
        else: 
            return node
    def parse_primary(self):
        print(f'curr: {self.peek()} from parse_primary') if DEBUG else None
        match self.peek().type:
            case Tktype.Integer:
                n = IntegerNode(int(self.peek().span))
                self.advance()
                return n
            case Tktype.Float:
                n = FloatNode(float(self.peek().span))
                self.advance()
                return n
            case Tktype.Id:
                id = self.peek().span
                self.advance()
                if self.peek().type == Tktype.Assing:
                    self.advance()
                    expr = self.parse_expr()
                    self.eat(Tktype.Semicolon)
                    return VarDecl(id,expr)
                return IdNode(id)
            case Tktype.BTrue:
                self.eat(Tktype.BTrue)
                return BoolNode(True)
            case Tktype.BFalse:
                self.eat(Tktype.BFalse)
                return BoolNode(False)
            case Tktype.String:
                value = self.peek().span[1:-1]
                self.eat(Tktype.String)
                return StringNode(value)
            case Tktype.Read:
                return self.parse_read()
            case Tktype.Nothing:
                self.advance()
                return NothingNode()
            case _:
                print(f"not implemented yet! :) (from parse_primary): curr_tk: {self.peek()}")
                exit(2)
    def parse(self):
        while self.peek().type != Tktype.Eof:
            self.ast.append(self.parse_decl())              

    