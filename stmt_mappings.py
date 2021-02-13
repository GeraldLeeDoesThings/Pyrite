import ast
import compiler
import warnings


def translate_function_def(astree: ast.FunctionDef, kwargs: dict) -> str:
    # TODO: Handle decorators and a whole lot of other stuff
    header = "fn " + astree.name + "("
    addcomma = ''
    for arg in astree.args.args:
        argname = arg.arg
        argtype = compiler.typemappings[arg.annotation.id]
        header = header + addcomma + argname + ': ' + argtype
        addcomma = ', '
    header = header + ') {\n'
    return header.join(['    ' + compiler.translate_stmt(x, kwargs) for x in astree.body]) + '\n}\n'


def translate_async_function_def(astree: ast.AsyncFunctionDef, kwargs: dict) -> str:
    return "async " + translate_function_def(
        # for now, almost the same as function def
        ast.FunctionDef(astree.name, astree.args, astree.body,
                        astree.decorator_list, astree.returns,
                        astree.type_comment), kwargs)


def translate_class_def(astree: ast.ClassDef, kwargs: dict) -> str:
    name = astree.identifier
    # TODO: Keywords, decorators, inheritance ("bases")
    classtext = 'struct ' + name + ';\nimpl ' + name + ' {\n'
    classtext = classtext.join(['   ' + compiler.translate_stmt(x, kwargs) for x in astree.body])
    return classtext + '\n}\n'


def translate_return(astree: ast.Return, kwargs: dict) -> str:
    return 'return ' + compiler.translate_expr(astree.value, kwargs) + ';\n'


def translate_delete(astree: ast.Delete, kwargs: dict) -> str:
    warnings.warn("Keyword del is not supported")  # TODO: Make more descriptive
    return ''


def translate_assign(astree: ast.Assign, kwargs: dict) -> (str, dict):
    var_table = kwargs.get('var_table', default=set())
    targets = []
    value = compiler.translate_expr(astree.value, kwargs)
    result = ''
    for target in astree.targets:
        name = compiler.translate_expr(target, kwargs)
        targets.append(name)
        if name in var_table:
            result = result + name + ' = ' + value + ';\n'
        else:
            # TODO: Detect constants
            result = result + 'let mut ' + name + ' = ' + value + ';\n'
            var_table.add(name)
            kwargs['var_table'] = var_table
    return result, kwargs
