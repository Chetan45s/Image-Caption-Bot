#https://ide.geeksforgeeks.org/nV25VSh6BK
import lang.lexer
from lang.lexer import def_var, RTError
import lang.parser_
from lang.parser_ import NumberNode,BinOpNode,UnOpNode


class RTResult:

    def __init__(self):
        self.value = None
        self.error = None

    def register(self,res):
        if res.error:
            self.error = res.error
        return res.value
    
    def success(self,value):
        self.value = value
        return self
    
    def failure(self,error):
        self.error = error
        return self

class Number:
    
    def __init__(self,value):
        self.value = value
        self.set_pos()

    def set_pos(self,pos_start=None,pos_end=None):
        self.pos_start = pos_start
        self.pos_end = pos_end
    
    def added_to(self, other):
        if isinstance(other, Number):
            return Number(self.value + other.value), None
    
    def subtracted_to(self,other):
        if isinstance(other, Number):
            return Number(self.value - other.value), None

    def multiplied_to(self,other):
        if isinstance(other, Number):
            return Number(self.value * other.value), None

    def divided_to(self,other):
        if isinstance(other, Number):
            if other.value == 0:
                return None, RTError(other.pos_start, other.pos_end,"Division by zero")
            return Number(self.value/other.value), None

    def __repr__(self):
        return str(self.value)

class Interpreter:
    
    def visit(self,node):
        method_name = f"visit_{type(node).__name__}"
        method = getattr(self, method_name,self.no_visit_method)
        return method(node)
    
    def no_visit_method(self):
        raise Exception(f"No visit_{type(node).__name__} method defined")
    
    def visit_NumberNode(self,node):
        res = RTResult()
        som = Number(node.tok.value)
        som.set_pos(node.pos_start,node.pos_end)
        return res.success(som)
    
    def visit_BinOpNode(self,node):
        res = RTResult()
        left = res.register(self.visit(node.left_node))
        if res.error:
            return res
        right = res.register(self.visit(node.right_node))
        if res.error:
            return res

        if node.op_tok.type == def_var['TT_PLUS']:
            result, error = left.added_to(right)    
        elif node.op_tok.type == def_var['TT_MINUS']:
            result, error = left.subtracted_to(right)
        elif node.op_tok.type == def_var['TT_MUL']:
            result, error = left.multiplied_to(right)
        elif node.op_tok.type == def_var['TT_DIV']:
            result, error = left.divided_to(right)
        
        if error:
            return res.failure(error)
        else:
            result.set_pos(node.pos_start,node.pos_end)
            return res.success(result)
    
    def visit_UnOpNode(self,node):
        res = RTResult()
        error = None
        number = res.register(self.visit(node.node))
        if res.error:
            return res

        if node.op.type == def_var['TT_MINUS']:
            number, error = number.multiplied_to(Number(-1))
        
        if error:
            return res.failure(error)
        else:
            number.set_pos(node.pos_start,node.pos_end)
            return res.success(number)
        
def run(node):
    iter = Interpreter()
    result = iter.visit(node)
    return result