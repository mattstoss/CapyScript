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
            env.declare(node.name, result)
        elif isinstance(node, ast.Identifier):
            return env.get(node.value)
        elif isinstance(node, ast.String):
            return node.value
        elif isinstance(node, ast.Assignment):
            value = self._execute_impl(node.expr, env)

            if isinstance(node.name, ast.GetProperty):
                instance = self._execute_impl(node.name.instance, env)
                assert isinstance(instance, runtime.Instance)

                instance.data[node.name.property] = value
                return value

            return env.assign(node.name.value, value)
        elif isinstance(node, ast.Print):
            result = self._execute_impl(node.expr, env)
            print(result)
        elif isinstance(node, ast.GetProperty):
            instance = self._execute_impl(node.instance, env)
            if node.property in instance.data:
                return instance.data[node.property]
            for func_decl in instance.parent.body:
                if func_decl.name == node.property:

                    def bound_method(*args):
                        call_env = Environment(enclosing_env=env)
                        call_env.declare("self", instance)
                        return self._execute_impl(func_decl.body, call_env)

                    return bound_method
            raise ValueError(f"interpreter: failed to get property {node.property}")
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
            env.declare(node.name, callable)
        elif isinstance(node, ast.ClassDecl):
            callables = []
            for func_decl in node.body:
                new_callable = runtime.Callable(
                    func_decl.name, func_decl.body, func_decl.params
                )
                callables.append(new_callable)
            class_decl = runtime.Class(node.name, callables)
            env.declare(node.name, class_decl)
        elif isinstance(node, ast.Call):
            value = self._execute_impl(node.value, env)
            if isinstance(value, runtime.Class):
                parent_class = value
                instance = runtime.Instance(parent_class, dict())
                return instance

            if hasattr(value, "__name__") and value.__name__ == "bound_method":
                bound_method = value
                return bound_method(*node.args)

            callable = value
            if not isinstance(value, runtime.Callable):
                raise ValueError(f"interpreter: not callable: [{type(callable)}]")
            if len(callable.params) != len(node.args):
                raise ValueError(
                    f"interpreter: {callable.name} requires exactly {len(callable.params)} arguments but {len(node.args)} provided"
                )
            call_env = Environment(enclosing_env=env)
            for param, arg in zip(callable.params, node.args):
                arg_value = self._execute_impl(arg.expr, env)
                call_env.declare(param.name, arg_value)
            return self._execute_impl(callable.body, call_env)
        else:
            raise ValueError(f"interpreter: unexpected node [{type(node)}]")
