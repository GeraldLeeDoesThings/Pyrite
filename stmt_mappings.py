import ast
import copy
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
    header = header + ') -> ' + compiler.typemappings[astree.type_comment] + ' {\n'
    body = ''
    inner_kwargs = copy.deepcopy(kwargs)
    for node in astree.body:
        source, inner_kwargs = compiler.translate_stmt(node, inner_kwargs)
        body = body + source
    return header + body + '\n}\n'


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
    classbody = ''
    inner_kwargs = copy.deepcopy(kwargs)
    for node in astree.body:
        source, inner_kwargs = compiler.translate_stmt(node, inner_kwargs)
        classbody = classbody + source
    return classtext + classbody + '\n}\n'


def translate_return(astree: ast.Return, kwargs: dict) -> str:
    return 'return ' + compiler.translate_expr(astree.value, kwargs) + ';\n'


def translate_delete(astree: ast.Delete, kwargs: dict) -> str:
    warnings.warn("Keyword del is not supported")  # TODO: Make more descriptive
    return ''


def translate_assign(astree: ast.Assign, kwargs: dict) -> str:
    # No deepcopy since we want to remember variable assignment
    var_table = kwargs.get('var_table', default=set())
    targets = []
    value = compiler.translate_expr(astree.value, kwargs)
    result = ''
    for target in astree.targets:
        name, _ = compiler.translate_expr(target, kwargs)
        targets.append(name)
        if name in var_table:
            result = result + name + ' = ' + value + ';\n'
        else:
            # TODO: Detect constants
            result = result + 'let mut ' + name + ' = ' + value + ';\n'
            var_table.add(name)
            kwargs['var_table'] = var_table
    return result
