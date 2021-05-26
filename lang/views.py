from django.shortcuts import render
from django.shortcuts import get_object_or_404
from lang.forms import LangForm
from PIL import Image  
import base64
import io
from lang.basic import lang_fun

def lang(request):
    lang_form = LangForm()
    if request.method == 'POST':
        lang_form = LangForm(request.POST)
        if lang_form.is_valid():
            Input = lang_form.cleaned_data['expr']
            token,error,ast_node,ast_error,output,output_error = lang_fun(Input)
            if error:
                error = error.as_string()
            if ast_error:
                ast_error = ast_error.as_string()
            if output_error:
                output_error = output_error.as_string()
            context = {
                'Input' : Input,
                'Tokens' : token,
                'Tokens_error' : error,
                'AST' : ast_node,
                'AST_error' : ast_error,
                'Output' : output,
                'Output_error' : output_error,
            }
            return render(request, 'lang1.html',context)
    return render(request, 'lang.html',{'lang_form':lang_form})
