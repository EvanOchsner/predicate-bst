"""Example usage of the predicate_to_bst package."""

import json
from predicate_to_bst import build_boolean_syntax_tree

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
        print()

if __name__ == "__main__":
    main()
