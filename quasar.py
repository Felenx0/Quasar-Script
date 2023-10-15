from sys import *
from quasarC import *

def open_file(file_name):
    data = open(file_name).read()
    return data + '<EOF>'

def run():
    isDot = False
    dotType = ''
    for check in argv[1]:
        if check == '.':
            isDot = True
        elif isDot:
            dotType += check
    
    if dotType == 'qs':
        text = open_file(argv[1])

        lexer = lex(text)
        parse(lexer)
    else:
        print('Incorrect file type.')

run()