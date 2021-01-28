import ast
import compiler


def translate_module(astree: ast.Module) -> str:
    return "".join([compiler.translate_stmt(x) for x in astree.body])


def translate_interactive(astree: ast.Interactive) -> str:
    return "".join([compiler.translate_stmt(x) for x in astree.body])


def translate_expression(astree: ast.Expression) -> str:
    return compiler.translate_expr(astree.body)

