###############################################################################

# Lexer : Inputs the raw code and convert it into a stream of tokens

################################################################################

from lang.string_with_arrow import string_with_arrows

"""
Declaring Strings to represent Data Types and operands
"""
def_var = {
    'TT_INT' : 'INT',
    'TT_FLOAT' : 'FLOAT',
    'TT_PLUS' : 'PLUS',
    'TT_MINUS' :  'MINUS',
    'TT_MUL' : 'MUL',
    'TT_DIV' : 'DIV',
    'TT_LPAREN' : 'LPAREN',
    'TT_RPAREN' : 'RPAREN',
    'DIGITS' : "0123456789",
    'TT_EOF' : 'EOF',
}

"""

Token Class

Input : type of the operand or datatype and value of datatype

"""
class Token:

    def __init__(self,type_,value=None,pos_start=None,pos_end=None):
        self.type = type_
        self.value = value

        if pos_start:
            self.pos_start = pos_start.copy()
            self.pos_end = pos_start.copy()
            self.pos_end.advance()
        if pos_end:
            self.pos_end = pos_end
    
    def __repr__(self):

        """
        if the "type" is Datatype then it has some value so we check whether we are
        getting the value or not. __repr__ function is used for to return the string
        in well representation.

        """

        if self.value:
            return f"{self.type}:{self.value}"
        else:
            return f"{self.type}"


"""
Classes for Error handling

Whenever a chance of error occur we call this class with error details
to be returned to the user

"""

class Error:

    def __init__(self,error_name,pos_start,pos_end,details):
        self.pos_start = pos_start
        self.pos_end = pos_end
        self.error_name = error_name
        self.details = details

    def as_string(self):
        result =  f'{self.error_name}: {self.details}'
        result += f"\nFile {self.pos_start.file}, line {self.pos_start.line + 1}"
        result += '\n\n' + string_with_arrows(self.pos_start.file_line, self.pos_start, self.pos_end)
        return result

class InvalidCharError(Error):

    def __init__(self,pos_start,pos_end,details):
        super().__init__('InValid Character Given',pos_start,pos_end,details)

class InvalidSyntaxError(Error):
    
    def __init__(self,pos_start,pos_end,details=''):
        super().__init__('Invalid Syntax',pos_start,pos_end,details)

class RTError(Error):
    
    def __init__(self,pos_start,pos_end,details=''):
        super().__init__('Runtime Error',pos_start,pos_end,details)

###############################
# Position of the error
###############################


class Position:

    def __init__(self,idx,line,col,file=None, file_line=None):
        self.idx = idx
        self.line = line
        self.col = col
        self.file_line = file_line
        self.file = file
    
    ############
    # In this advance method we are incrementing Line, Col
    def advance(self, current_char=None):
        self.idx += 1
        self.col += 1

        if current_char == '\n':
            self.line += 1
            self.col = 0

        return self

    def copy(self):
        # return all the information about the current position whenever called
        return Position(self.idx,self.line,self.col,self.file,self.file_line)



"""
Lexer class

Here we are iterating over all the code/text of the user and
taking tokens out of that 
"""

class Lexer:

    def __init__(self,file,text):
        self.file = file
        self.text = text
        self.pos = Position(-1,0,-1,file,text)
        self.current_char = None
        self.advance()


    """
    This method increment the value of the pos of the pointer and store the
    current_char of poining pos. 

    If we are at the end of the text/code then it will return None
    """
    def advance(self):
        self.pos.advance(self.current_char)
        if self.pos.idx < len(self.text):
            self.current_char = self.text[self.pos.idx]
        else:
            self.current_char = None


    """
    Creating and storing tokens in the token list and calling
    Token class (Defined Above) to get a well representation.
    """
    def make_tokens(self):

        tokens = []

        while self.current_char != None:

            if self.current_char in ' \t':
                self.advance()
            elif self.current_char == '+':
                tokens.append(Token(def_var['TT_PLUS'],pos_start=self.pos))
                self.advance()
            elif self.current_char == '-':
                tokens.append(Token(def_var['TT_MINUS'],pos_start=self.pos))
                self.advance()
            elif self.current_char == '*':
                tokens.append(Token(def_var['TT_MUL'],pos_start=self.pos))
                self.advance()
            elif self.current_char == '/':
                tokens.append(Token(def_var['TT_DIV'],pos_start=self.pos))
                self.advance()
            elif self.current_char == '(':
                tokens.append(Token(def_var['TT_LPAREN'],pos_start=self.pos))
                self.advance()
            elif self.current_char == ')':
                tokens.append(Token(def_var['TT_RPAREN'],pos_start=self.pos))
                self.advance()
            elif self.current_char in def_var['DIGITS']:
                """
                Here the digit can be of any length so we need to def
                seperate class to check the data type of number and also
                whether it is a valid number or not.
                """
                # print(self.pos)
                tokens.append(self.make_number())
                # print(self.pos)

            else:
                """ERROR"""
                pos_start = self.pos.copy()
                char = self.current_char # store the invalid char
                self.advance()
                pos_end = self.pos
                return [] ,InvalidCharError(pos_start,pos_end,"'" + char + "'") # so we need to return empty list of tokens and error details
        # if no error occurs then return None in case of error 
        tokens.append(Token(def_var['TT_EOF'],pos_start=self.pos))
        return tokens,None
        
    def make_number(self):

        num_str = ''
        dot_count = 0
        pos_start = self.pos.copy()

        # if current_char is still a digit or a dot
        while self.current_char != None and self.current_char in def_var['DIGITS'] + '.':

            if self.current_char == '.':
                # more then one dot in a number is not possible so break
                """ERROR"""
                if dot_count == 1:
                    break
                dot_count += 1
                num_str += '.'
            else:
                num_str += self.current_char
            self.advance()
            
        if dot_count == 0:
            return Token(def_var['TT_INT'], int(num_str),pos_start,self.pos)
        else:
            return Token(def_var['TT_FLOAT'], float(num_str),pos_start,self.pos)


def run(file,text):
    lexer = Lexer(file,text)
    tokens,error = lexer.make_tokens()
    return tokens,error