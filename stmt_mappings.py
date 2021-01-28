import ast
import compiler


def translate_functiondef(astree: ast.FunctionDef) -> str:
    # TODO: Handle decorators and a whole lot of other stuff
    header = "fn " + astree.name + "("
    addcomma = ''
    for arg in astree.args.args:
        argname = arg.arg
        argtype = compiler.typemappings[arg.annotation.id]
        header = header + addcomma + argname + ': ' + argtype
        addcomma = ', '
    header = header + '\n'
    return header.join(['    ' + compiler.translate_stmt(x) for x in astree.body])



