from lang.lexer import run
from lang.parser_ import create_ast
from lang.Interpreter_ import run as run2
# def printout(*args):
#     for itr in args:
#         if itr: print(itr)

# while True:
    # text = input("-> ")
def lang_fun(text):
    token,error,ast_node,ast_error,output,output_error = None,None,None,None,None,None
    tokens, error = run("Shell",text)
    token = tokens
    if error is not None:
        return token,error,ast_node,ast_error,output,output_error
        # print(error.as_string())
    # Generate Absract Syntax Tree
    else:
        ast = create_ast(tokens)
        if ast.error:
            return token,error,ast_node,ast.error,output,output_error
            # print(ast.node,ast.error.as_string())
        else:
            # print(ast.node)
            interprrter = run2(ast.node)
            ast_node = ast.node
            if interprrter.error:
                return token,error,ast_node,ast_error,output,interprrter.error
                # print(interprrter.error.as_string())
            else:
                # print(interprrter.value)
                return token,error,ast_node,ast_error,interprrter.value,None
                # return tokens,ast.node,interprrter.value,interprrter.error          
    return token,error,ast_node,ast_error,output,output_error
