import re
class Tktype:
                                # Keywords
    Var = "Var"
    If = "If"
    Else = "Else"
    Print = "Print"
    Read = "Read"

    String = "String"
    Lbrace = "Lbrace"
    Rbrace = "Rbrace"
    Id = "Id"
    Assing = "Assing"
    Integer = "Integer"
    Float = "Float"
    BTrue = "True"
    BFalse = "False"
    Eq = "Eq"
    Ne ="Ne"
    Gt = "Gt"
    Lt = "Le"
    Ge = "Ge"
    Le = "Le"
    Plus = "Plus"
    Minus = "Minus"
    Star = "Star"
    Slash = "Slash"
    Semicolon = "Semicolon"
    Nothing = "Nothing"
    Eof = "Eof"

class Tk:
    def __init__(self, type, span):
        self.type = type
        self.span = span
    def __repr__(self):
        return f"Token {self.type} >> '{self.span}'\n"
    
class Lexer:
    def __init__(self,code):
        self.code = code
        self.pos = 0
        self.tokens:list[Tk] = []
    def jump_space(self):
        while True:
            if self.pos < len(self.code):
                if self.code[self.pos]==" ":
                    #print("hi!")
                    self.pos += 1
                    continue
                elif self.code[self.pos]=="\n":
                    #print("hi!")
                    self.pos += 1
                    continue
                elif self.code[self.pos:self.pos+2] == "//":
                    self.pos += 2
                    while self.pos < len(self.code):
                        if self.code[self.pos] == "\n": 
                            break
                        else:
                            self.pos += 1
                else: break
            else: break
    def lexer(self):
        regexs = {
            '(?P<val>var )':Tktype.Var,
            '(?P<val>if )': Tktype.If,
            '(?P<val>else )': Tktype.Else,
            '(?P<val>print )': Tktype.Print,
            '(?P<val>read )':Tktype.Read,
            '(?P<val>nothing)':Tktype.Nothing,
            '(?P<val>\\+)': Tktype.Plus,
            '(?P<val>-)':Tktype.Minus,
            '(?P<val>\\*)':Tktype.Star,
            '(?P<val>/)':Tktype.Slash,
            '(?P<val>==)':Tktype.Eq,
            "(?P<val>!=)":Tktype.Ne,
            "(?P<val>>=)":Tktype.Ge,
            "(?P<val><=)":Tktype.Le,
            "(?P<val>>)":Tktype.Gt,
            "(?P<val><)":Tktype.Lt,
            '(?P<val>=)':Tktype.Assing,
            '(?P<val>;)':Tktype.Semicolon,
            '(?P<val>{)':Tktype.Lbrace,
            '(?P<val>})':Tktype.Rbrace,
            '(?P<val>\\d+\\.\\d+)':Tktype.Float,
            "(?P<val>\\d+)":Tktype.Integer,
            "(?P<val>true)":Tktype.BTrue,
            "(?P<val>false)":Tktype.BFalse,
            '(?P<val>"[^"]*")':Tktype.String,
            '(?P<val>[a-zA-Z_]\\w*)':Tktype.Id,
        }
        while True:
            if self.pos == len(self.code):
                if self.tokens[-1].type != Tktype.Eof:
                    self.tokens.append(Tk(Tktype.Eof,""))
                break
            else: pass
            for reg in regexs:
                if self.pos == len(self.code):
                    self.tokens.append(Tk(Tktype.Eof,""))
                    break
                self.jump_space()
                #print(reg)
                mat = re.match(reg, self.code[self.pos:])
                if isinstance(mat,re.Match): 
                    self.tokens.append(Tk(regexs[reg],mat.group("val")))
                    self.pos += mat.span("val")[1]
                    break
                else: continue
            else:
                print(f"error: unknown caracter: `{self.code[self.pos]}`")
                exit(1)
            continue