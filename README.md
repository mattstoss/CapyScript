# CapyScript

## Todo List

1. Implement lambdas / first-class function support. For instance, allowing functions to capture local variables and return functions. The main problem is that we are considering "FuncDecl" to be a statement, but variable declaration and return statements expect an expr. I'm pretty sure merely modifying the ast, parser, and interpreter to consider  `FuncDecl` as a `ExprNode` instead of a `StmtNode` should be able to fix this.
1. Implement multi-line comments
1. Add support for number type
1. Add support for string type
1. Add support for boolean type
1. Add support for nil type