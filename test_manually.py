#!/usr/bin/env python
"""Simple script to manually test the predicate_to_bst package."""

import sys
from predicate_to_bst.parser import tokenize, build_boolean_syntax_tree, TokenType

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
    
    print("\nAll tests passed!")
    return 0

if __name__ == "__main__":
    sys.exit(main())
