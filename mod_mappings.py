import ast
import compiler


def translate_module(astree: ast.Module, **kwargs) -> str:
    return "".join([compiler.translate_stmt(x, kwargs) for x in astree.body])


def translate_interactive(astree: ast.Interactive, **kwargs) -> str:
    return "".join([compiler.translate_stmt(x, kwargs) for x in astree.body])


def translate_expression(astree: ast.Expression, **kwargs) -> str:
    return compiler.translate_expr(astree.body, kwargs)

