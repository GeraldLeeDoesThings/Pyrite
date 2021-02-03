import ast
import mod_mappings
import stmt_mappings
import expr_mappings


typemappings = dict(
    {'int': 'i32'}
)


def parse_source(source: str) -> ast.AST:
    return ast.parse(source, mode="exec", type_comments=True)


def parse_file(filename: str) -> ast.AST:
    with open(filename, 'r') as file:
        return ast.parse(source="".join([x + '\n' for x in file.readlines()],),
                         filename=filename,
                         mode="exec",
                         type_comments=True)


def translate_mod(astree: ast.AST, kwargs: dict) -> str:
    atype = astree.__class__
    if atype == ast.Module:
        return mod_mappings.translate_module(astree, kwargs)
    elif atype == ast.Interactive:
        return mod_mappings.translate_interactive(astree, kwargs)
    elif atype == ast.Expression:
        return mod_mappings.translate_expression(astree, kwargs)
    return ""


def translate_stmt(astree: ast.AST, kwargs: dict) -> str:
    return ""


def translate_expr(astree: ast.AST, kwargs: dict) -> str:
    return ""
