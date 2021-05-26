###################################################################

# Parser Returns the Tree of tokens which means in which way
# compution should be done

###################################################################

import lang.lexer
from lang.lexer import def_var,Error,InvalidSyntaxError

"""
ParseResult keep track of all the error while parsing the 
tokens

"""
class ParseResult:
    def __init__(self):
        self.error = None
        self.node = None

    def register(self,res):

        # checking whether res is instance of PraseResult class or not
        if isinstance(res,ParseResult):
            # if yes then we check for error 
            if res.error:
                self.error = res.error
            return res.node
        return res

    
    def success(self,node):
        self.node = node
        return self

    def failure(self,error):
        self.error = error
        print(self.error)
        return self


"""
NumberNode

returns the token in string form

BinOpNode

Return the operation in string format
"""
class NumberNode:

    def __init__(self,tok):
        self.tok = tok
        self.pos_start = self.tok.pos_start
        self.pos_end = self.tok.pos_end

    def __repr__(self):
        return f"{self.tok}"

class BinOpNode:

    def __init__(self,left_node,op_tok,right_node):
        self.left_node = left_node
        self.op_tok = op_tok
        self.right_node = right_node
        self.pos_start = self.left_node.pos_start
        self.pos_end = self.right_node.pos_end

    def __repr__(self):
        return f"({self.left_node}, {self.op_tok}, {self.right_node})"

class UnOpNode:

    def __init__(self,op,node):
        self.node = node
        self.op = op
        self.pos_start = self.op.pos_start
        self.pos_end = self.node.pos_end
    def __repr__(self):
        return f"({self.op},{self.node})"
"""

Parser 

Just like tokens it check for parity and create a 
parser tree

"""

class Parser:
    """
    Same as we did for the lexer, we do here
    initialize the tok_idx to -1 and iterate over the tokens using advance() function
    """
    def __init__(self,tokens):
        self.tokens = tokens
        self.tok_idx = -1
        # self.current_tok = None
        self.advance()

    """
    take tok_idx and check whether it is in range if yes then return
    the current_tok
    """
    def advance(self):
        self.tok_idx += 1
        if self.tok_idx < len(self.tokens):
            self.current_tok = self.tokens[self.tok_idx]
        # print(self.current_tok.type)
        return self.current_tok

    #######################################
    """
    we have seen the function to iterate over the tokens but now we
    have to generate the Abstract Syntax Tree from the tokens for this 
    we use factor, term, expr functions.


    Grammer :

    Whenever we parse over the mathematical operations first thing is to consider the 
    parity of the operands MUL/DIV > PLUS/MINUS
    """

    # Factors checks and returns the type of the integer
    # in a string representation by calling NumberNode class 
    def factor(self):
        res = ParseResult()
        tok = self.current_tok

        if tok.type in (def_var['TT_PLUS'],def_var['TT_MINUS']):
            res.register(self.advance())
            factor = res.register(self.factor())
            if res.error:
                return res
            return res.success(UnOpNode(tok,factor))

        elif tok.type in (def_var['TT_INT'],def_var['TT_FLOAT']):
            res.register(self.advance())
            return res.success(NumberNode(tok))

        elif tok.type == def_var['TT_LPAREN']:
            res.register(self.advance())
            expr = res.register(self.expr())
            if res.error:
                return res
            if self.current_tok.type == def_var['TT_RPAREN']:
                res.register(self.advance())
                return res.success(expr)
            else:
                return res.failure(InvalidSyntaxError(
                    self.current_tok.pos_start, self.current_tok.pos_end,"Expected ')'"
                ))

        """
        If in case tok.type doesn't belong anyone of them then
        return an error using InvalidSyntaxError class
        """
        return res.failure(InvalidSyntaxError(
            tok.pos_start, tok.pos_end,"Expected int or float"
        ))

    # this function check for DIV/MUL operands and if found then returns the
    # BinOpNode of that in the form of (INT:5,MUL/DIV,INT:6) and later on this
    # is used in reight or left term while forming the expression
    def term(self):
        return self.bin_op(self.factor, (def_var['TT_MUL'],def_var['TT_DIV']))
    
    def expr(self):
        return self.bin_op(self.term, (def_var['TT_PLUS'],def_var['TT_MINUS']))
    
    def bin_op(self,func,ops):
        res = ParseResult()
        left = res.register(func()) # check whether the factor function worked properly or not if not then return thee error
        if res.error:
            return res

        while self.current_tok.type in ops:
            op_tok = self.current_tok
            res.register(self.advance())
            right = res.register(func())
            if res.error:
                return res
            left = BinOpNode(left,op_tok,right)
        return res.success(left)

    def parse(self):
        res = self.expr()
        # print(res.node,res.error)
        if not res.error and self.current_tok.type != def_var['TT_EOF']:
            return res.failure(InvalidSyntaxError(
                self.current_tok.pos_start,self.current_tok.pos_end,"Expected '+','-','*' or '/'"
            ))
        return res
    ########################





def create_ast(tokens):
    p = Parser(tokens)
    return p.parse()