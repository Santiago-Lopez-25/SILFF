import parser
from lexer import Tktype

class Interpreter:
    def __init__(self,ast):
        self.ast = ast
        self.vars = {}
    def visit(self,node):
        method = getattr(self, f'visit_{type(node).__name__}')
        return method(node)
    def visit_IntegerNode(self,node):
        return node.value
    def visit_FloatNode(self,node):
        return node.value
    def visit_StringNode(self,node):
        return node.value
    def visit_BoolNode(self,node):
        return node.value
    def visit_BlockNode(self,node):
        for stat in node.stats:
            if stat is not None:
                self.visit(stat)
    def visit_VarDecl(self,node):
        value = self.visit(node.value)
        self.vars[node.name] = value
    def visit_IdNode(self,node):
        return self.vars[node.id]
    def visit_BinOpNode(self,node):
        lhs = self.visit(node.left)
        rhs = self.visit(node.rigth)
        match node.op:
            case Tktype.Plus:
                return lhs + rhs
            case Tktype.Minus:
                return lhs - rhs
            case Tktype.Star:
                return lhs * rhs
            case Tktype.Slash:
                if rhs == 0:
                    print("error: cannot divide by zero")
                    exit(2)
                return lhs / rhs
            case Tktype.Lt:
                return lhs < rhs
            case Tktype.Gt:
                return lhs > rhs
            case Tktype.Le:
                return lhs <= rhs
            case Tktype.Ge:
                return lhs >= rhs
            case Tktype.Ne:
                return lhs != rhs
            case Tktype.Eq:
                return lhs == rhs
    def visit_IfNode(self,node):
        expr = self.visit(node.condition)
        if expr is not None:
            if expr:
                self.visit(node.block)  
            else:
                if node.eblock is not None:
                    self.visit(node.eblock)
    def visit_PrintNode(self,node):
        expr = self.visit(node.expr)
        print(expr)
    def visit_ReadNode(self,node):
        read = input(node.msg.value)
        return read
    def visit_NothingNode(self,node): pass
    def evaluate(self): 
        for stat in self.ast:
            self.visit(stat)  