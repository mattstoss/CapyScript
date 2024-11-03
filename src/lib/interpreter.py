from lib import ast
from lib import runtime
from lib.environment import Environment


class Interpreter:
    def __init__(self, nodes):
        self._nodes = nodes

    def execute(self):
        self._execute_impl(ast.Block(self._nodes), None)

    def _execute_impl(self, node, env):
        if isinstance(node, ast.VarDecl):
            result = self._execute_impl(node.expr, env)
            env.set(node.name, result)
        elif isinstance(node, ast.Identifier):
            return env.get(node.value)
        elif isinstance(node, ast.String):
            return node.value
        elif isinstance(node, ast.Print):
            result = self._execute_impl(node.expr, env)
            print(result)
        elif isinstance(node, ast.Return):
            return self._execute_impl(node.expr, env)
        elif isinstance(node, ast.Block):
            block_env = Environment(enclosing_env=env)
            last_result = None
            for node in node.nodes:
                last_result = self._execute_impl(node, block_env)
            return last_result
        elif isinstance(node, ast.FuncDecl):
            callable = runtime.Callable(node.name, node.body, node.params)
            env.set(node.name, callable)
        elif isinstance(node, ast.Call):
            callable = self._execute_impl(node.value, env)
            if not isinstance(callable, runtime.Callable):
                raise ValueError(f"interpreter: not callable: [{type(callable)}]")
            if len(callable.params) != len(node.args):
                raise ValueError(
                    f"interpreter: {callable.name} requires exactly {len(callable.params)} arguments but {len(node.args)} provided"
                )
            call_env = Environment(enclosing_env=env)
            for param, arg in zip(callable.params, node.args):
                arg_value = self._execute_impl(arg.expr, env)
                call_env.set(param.name, arg_value)
            return self._execute_impl(callable.body, call_env)
        else:
            raise ValueError(f"interpreter: unexpected node [{type(node)}]")
