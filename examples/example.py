"""Example usage of the predicate_to_bst package."""

import json
from predicate_to_bst import build_boolean_syntax_tree, convert_to_polars

def main():
    """Run examples of building Boolean syntax trees from expressions."""
    examples = [
        '@.key1 == "value1" && @.key2 != "value2"',
        '@.k1 == "v1" || (@.k2 == "v2" && (@.k3 >= 1.1 || @.k4 < 0))',
        '@.price > 150.35'
    ]

    for i, expr in enumerate(examples, 1):
        print(f"Example {i}: {expr}")
        tree = build_boolean_syntax_tree(expr)
        print(f"Tree structure: {tree}")
        print(f"Dictionary representation: {json.dumps(tree.to_dict(), indent=2)}")
        print("\nASCII Tree Visualization:")
        print(tree.to_ascii())
        
        print("\nPolars Expression:")
        polars_expr = convert_to_polars(expr)
        print(polars_expr)
        print("\n" + "="*50 + "\n")

if __name__ == "__main__":
    main()
