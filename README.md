# CapyScript

## Todo List

1. Implement variable reassignment. Right now, we can only define varaibles with `let a = ..`. CapyScript does permit shadowing, so we can `let a = ..` multiple times in the same scope, and it will rebind `a` with a new initial value. However, if we've already `let a = ..` once, we should be allowed to reassignment merely with `a = ..`
1. Implement lambdas / first-class function support. For instance, allowing functions to capture local variables and return functions. The main problem is that we are considering "FuncDecl" to be a statement, but variable declaration and return statements expect an expr. I'm pretty sure merely modifying the ast, parser, and interpreter to consider  `FuncDecl` as a `ExprNode` instead of a `StmtNode` should be able to fix this.
1. Implement multi-line comments
1. Add support for number type
1. Add support for string type
1. Add support for boolean type
1. Add support for nil type