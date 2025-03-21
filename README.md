# Predicate to Boolean Syntax Tree

A Python library for converting logical expressions into Boolean syntax trees.

## Features

- Parse logical expressions with AND (`&&`), OR (`||`), parentheses, and conditions
- Handle operator precedence (AND > OR) and parenthesized expressions
- Generate a structured syntax tree for further processing
- Convert trees to a dictionary representation for serialization

## Installation

```bash
# Install from PyPI (when published)
pip install predicate-to-bst

# Install from source
git clone https://github.com/yourusername/predicate_to_bst.git
cd predicate_to_bst
pip install -e .

# Install with development dependencies
pip install -e ".[dev]"
```

## Usage

```python
from predicate_to_bst import build_boolean_syntax_tree

# Simple expression
expression1 = '@.key1 == "value1" && @.key2 != "value2"'
tree1 = build_boolean_syntax_tree(expression1)
print(tree1)  # AND(Condition(@.key1 == "value1"), Condition(@.key2 != "value2"))

# Complex expression with nested operators
expression2 = '@.k1 == "v1" || (@.k2 == "v2" && (@.k3 >= 1.1 || @.k4 < 0))'
tree2 = build_boolean_syntax_tree(expression2)
print(tree2)

# Convert to dictionary for serialization
tree_dict = tree2.to_dict()
print(tree_dict)
```

## Supported Syntax

The parser can handle logical expressions with the following components:

1. `&&` - Logical AND operator
2. `||` - Logical OR operator
3. `(` and `)` - Parentheses for controlling associativity and precedence
4. Conditions - Arbitrary strings that will be treated as leaf nodes (e.g., `@.foo == "value"`)

Examples of valid expressions:

```
@.key1 == "value1" && @.key2 != "value2"
@.k1 == "v1" || (@.k2 == "v2" && (@.k3 >= 1.1 || @.k4 < 0))
@.price > 150.35
```

## Development

### Setup

```bash
# Clone the repository
git clone https://github.com/yourusername/predicate_to_bst.git
cd predicate_to_bst

# Install development dependencies
pip install -e ".[dev]"
```

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=predicate_to_bst
```

## License

MIT
