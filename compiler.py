import ast


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


def translate_mod(astree: ast.AST) -> str:
    return ""


def translate_stmt(astree: ast.AST) -> str:
    return ""


def translate_expr(astree: ast.AST) -> str:
    return ""
