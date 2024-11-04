# CapyScript

## Todo List

1. Implement lambdas / first-class function support. 

    > Note: For instance, allowing functions to capture local variables and return functions. The main problem is that we are considering "FuncDecl" to be a statement, but variable declaration and return statements expect an expr. I'm pretty sure merely modifying the ast, parser, and interpreter to consider  `FuncDecl` as a `ExprNode` instead of a `StmtNode` should be able to fix this.

1. Implement multi-line comments

1. Add support for types other than string

    1. Numbers
    1. Strings
    1. Boolean
    1. Nil

1. Improve support for class

    1. Add additional tests
    1. Implement constructors
    1. Fix weird method-binding hack
    1. Implement attr readers and writers for property access
    1. Implement private methods and properties
    1. Implement constructors
    1. Implement class variables
    1. Implement class functions
    1. Add ability to reference super

1. Implement a mark and sweep garbage collector

1. Fix assignment scoping bug

    > Note: For instance, global variables can't be assigned to in functions, because the environment assign method forgets to walk up the enclosing environment

1. Add control flow

    1. if / else statements
    2. else if
    3. for
    4. while

1. Add additional operaters

    1. Nested ()
    1. Logical and and or
    1. Equality: == and !=
    1. Other comparisan operators: <, <=, >=, >
    1. Subtraction and addition
    1. Multiplication and division

1. Code improvements

    1. Implement the visitor pattern
    1. Apply type hinting to more of the problem
    1. Move property resolution rules to a dedicated function on the Instance type
    1. Implement an AST pretty-printer
    1. Introduce a command-line tool

1. Error message improvements

    1. Start tracking line-of-code
    1. Attempt to start suggesting recoveries / fixes in the parser
    1. Implement a stack trace in the Interpreter

