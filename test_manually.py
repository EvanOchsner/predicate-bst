#!/usr/bin/env python
"""Simple script to manually test the predicate_to_bst package."""

import sys
from predicate_to_bst.parser import tokenize, build_boolean_syntax_tree, TokenType, to_polars_expr, convert_to_polars

def main():
    """Run a simple test of the predicate_to_bst functionality."""
    test_expression = '@.key1 == "value1" && @.key2 != "value2"'
    
    print(f"Testing expression: {test_expression}")
    print("\nTokenizing...")
    tokens = tokenize(test_expression)
    for i, token in enumerate(tokens):
        if token.type == TokenType.CONDITION:
            print(f"  Token {i+1}: {token.type.name} - '{token.value}'")
        else:
            print(f"  Token {i+1}: {token.type.name}")
    
    print("\nBuilding syntax tree...")
    tree = build_boolean_syntax_tree(test_expression)
    print(f"  Tree: {tree}")
    
    print("\nASCII representation of the tree:")
    print(tree.to_ascii())
    
    print("\nPolars expression:")
    polars_expr = to_polars_expr(tree)
    print(f"  {polars_expr}")
    
    # Test a more complex example
    complex_expression = '@.k1 == "v1" || (@.k2 == "v2" && (@.k3 >= 1.1 || @.k4 < 0))'
    print(f"\nTesting complex expression: {complex_expression}")
    complex_tree = build_boolean_syntax_tree(complex_expression)
    print("\nASCII representation of the complex tree:")
    print(complex_tree.to_ascii())
    
    print("\nPolars expression for complex tree:")
    complex_polars = convert_to_polars(complex_expression)
    print(f"  {complex_polars}")
    
    # Test numeric comparison
    numeric_expression = '@.price > 150.35 && @.quantity <= 10'
    print(f"\nTesting numeric expression: {numeric_expression}")
    numeric_tree = build_boolean_syntax_tree(numeric_expression)
    numeric_polars = to_polars_expr(numeric_tree)
    print("\nASCII representation:")
    print(numeric_tree.to_ascii())
    print("\nPolars expression:")
    print(f"  {numeric_polars}")
    
    print("\nAll tests passed!")
    return 0

if __name__ == "__main__":
    sys.exit(main())
