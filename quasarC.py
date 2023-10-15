import io

DIGITS = '0123456789.'
OPERATORS = '+-*/'

variables = {}

def lex(file_content):
    tok = ''
    string = ''
    expr = ''
    var_name = ''
    isStr = False
    isExpr = False
    
    tokens = []

    for char in file_content:
        tok += char
        
        if tok == ' ' and not isStr:
            if isVar:
                isVar = False
                tokens.append("VAR:" + var_name)
                var_name = ''
            tok = ''
        elif tok == '\n' or tok == '<EOF>':
            if expr != '':
                if isExpr:
                    tokens.append("EXPR:" + expr)
                    expr = ''
                else:
                    tokens.append("NUM:" + expr)
                    expr = ''
            elif isVar:
                isVar = False
                tokens.append("VAR:" + var_name)
                var_name = ''
            tok = ''
        elif tok in DIGITS and not isVar and not isStr:
            expr += tok
            tok = ''
        elif tok in OPERATORS and not isStr:
            isExpr = True
            expr += tok
            tok = ''
        elif tok == '$':
            isVar = True
        elif isVar and (tok != '=' or tok not in OPERATORS):
            var_name += tok
            tok = ''
        elif tok == '=':
            tokens.append("EQUALS")
            tok = ''
        elif tok == 'print':
            tokens.append("PRINT")
            tok = ''
        elif tok == '!print':
            tokens.append("!PRINT")
            tok = ''
        elif tok == "\"" and not isStr:
            #print("STRING START")
            isStr = True
            string = ''
            tok = ''
        elif isStr and tok != "\"":
            string += tok
            tok = ''
        elif tok == "\"" and isStr:
            tokens.append("STRING:" + string)
            isStr = False
            tok = ''
    
    print(tokens)
    return tokens

def parse(token):
    i = 0

    while i < len(token):
        #PRINT
        if token[i] + ' ' + token[i+1][0:6] == 'PRINT STRING' or token[i] + ' ' + token[i+1][0:4] == 'PRINT EXPR' or token[i] + ' ' + token[i+1][0:3] == 'PRINT NUM' or token[i] + ' ' + token[i+1][0:3] == 'PRINT VAR':
            if token[i+1][0:6] == 'STRING':
                print(token[i+1][7:], end='')
            elif token[i+1][0:4] == 'EXPR':
                print(eval(token[i+1][5:], end=''))
            elif token[i+1][0:3] == 'NUM':
                print(eval(token[i+1][4:]), end='')
            elif token[i+1][0:3] == 'VAR':
                print(variables[token[i+1][4:]], end='')
            i += 2
        #!PRINT
        elif token[i] + ' ' + token[i+1][0:6] == '!PRINT STRING' or token[i] + ' ' + token[i+1][0:4] == '!PRINT EXPR' or token[i] + ' ' + token[i+1][0:3] == '!PRINT NUM' or token[i] + ' ' + token[i+1][0:3] == '!PRINT VAR':
            if token[i+1][0:6] == 'STRING':
                print(token[i+1][7:])
            elif token[i+1][0:4] == 'EXPR':
                print(eval(token[i+1][5:]))
            elif token[i+1][0:3] == 'NUM':
                print(eval(token[i+1][4:]))
            elif token[i+1][0:3] == 'VAR':
                print(variables[token[i+1][4:]])
            
            i += 2
        #VAR CREATION
        elif token[i][0:3] + ' ' + token[i+1] + ' ' + token[i+2][0:6] == 'VAR EQUALS STRING' or token[i][0:3] + ' ' + token[i+1] + ' ' + token[i+2][0:3] == 'VAR EQUALS NUM' or token[i][0:3] + ' ' + token[i+1] + ' ' + token[i+2][0:4] == 'VAR EQUALS EXPR':
            if token[i+2][0:6] == 'STRING':
                variables[token[i][4:]] = token[i+2][7:]
            elif token[i+2][0:3] == 'NUM':
                variables[token[i][4:]] = eval(token[i+2][4:])
            elif token[i+2][0:4] == 'EXPR':
                variables[token[i][4:]] = eval(token[i+2][5:])
            
            i += 3
        else:
            i += 1
        
    #print(variables)