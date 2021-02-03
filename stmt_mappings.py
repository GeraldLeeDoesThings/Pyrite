import ast
import compiler


def translate_function_def(astree: ast.FunctionDef, kwargs: dict) -> str:
    # TODO: Handle decorators and a whole lot of other stuff
    header = "fn " + astree.name + "("
    addcomma = ''
    for arg in astree.args.args:
        argname = arg.arg
        argtype = compiler.typemappings[arg.annotation.id]
        header = header + addcomma + argname + ': ' + argtype
        addcomma = ', '
    header = header + '\n'
    return header.join(['    ' + compiler.translate_stmt(x, kwargs) for x in astree.body]) + '\n'


def translate_async_function_def(astree: ast.AsyncFunctionDef, kwargs: dict):
    return "async " + translate_function_def(
        # for now, almost the same as function def
        ast.FunctionDef(astree.name, astree.args, astree.body,
                        astree.decorator_list, astree.returns,
                        astree.type_comment), kwargs)
