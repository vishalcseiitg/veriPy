import ast

def unroll_loop(loop_node, unroll_factor):
    # Check that the loop is a for-loop with a range() call as its iterable
    if not isinstance(loop_node, ast.For):
        raise ValueError('Input node is not a for-loop.')
    if not isinstance(loop_node.iter, ast.Call) or not isinstance(loop_node.iter.func, ast.Name) or loop_node.iter.func.id != 'range':
        raise ValueError('Input node does not have a range() call as its iterable.')
    
    # Extract loop variables and range arguments
    loop_var = loop_node.target.id
    range_args = loop_node.iter.args
    
    # Check that the range() call has either one or two arguments
    if len(range_args) < 1 or len(range_args) > 2:
        raise ValueError('range() call does not have one or two arguments.')
    
    # Extract start, stop, and step values
    if len(range_args) == 1:
        start, stop, step = ast.Num(0), range_args[0], ast.Num(1)
    else:
        start, stop, step = range_args[0], range_args[1], ast.Num(1)
    
    # Calculate new range arguments based on unroll factor
    new_stop = ast.BinOp(stop, ast.Mult(), ast.Num(unroll_factor))
    new_step = ast.BinOp(step, ast.Mult(), ast.Num(unroll_factor))
    
    # Generate unrolled loop body
    unrolled_body = []
    for i in range(unroll_factor):
        body_copy = [ast.copy.deepcopy(n) for n in loop_node.body]
        for node in body_copy:
            for name, value in ast.walk(node):
                if isinstance(value, ast.Name) and value.id == loop_var:
                    value.id = f'{loop_var}_{i}'
        unrolled_body.extend(body_copy)
    
    # Generate new loop node with unrolled body and updated range arguments
    new_loop = ast.For(target=ast.copy.deepcopy(loop_node.target),
                       iter=ast.Call(func=ast.Name(id='range', ctx=ast.Load()),
                                     args=[start, new_stop, new_step],
                                     keywords=[]),
                       body=unrolled_body,
                       orelse=[])
    
    return new_loop

import ast

# Example Python code
python_code = """
def foo(n):
    for i in range(n):
        print(i)
"""
# Parse the Python code into an AST object
ast_obj = ast.parse(python_code)

# Print the AST object
print(ast.dump(ast_obj))

#Output

# Module(body=[FunctionDef(name='foo', args=arguments(posonlyargs=[], args=[arg(arg='n')], kwonlyargs=[], kw_defaults=[], defaults=[]), body=[For(target=Name(id='i', ctx=Store()), iter=Call(func=Name(id='range', ctx=Load()), args=[Name(id='n', ctx=Load())], keywords=[]), body=[Expr(value=Call(func=Name(id='print', ctx=Load()), args=[Name(id='i', ctx=Load())], keywords=[]))], orelse=[])], decorator_list=[])], type_ignores=[])
