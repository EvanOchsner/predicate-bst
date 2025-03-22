# Predicate to Boolean Syntax Tree

A Python library for converting logical expressions into Boolean syntax trees and target query languages.

## Features

- Parse logical expressions with AND (`&&`), OR (`||`), parentheses, and conditions
- Handle operator precedence (AND > OR) and parenthesized expressions
- Generate a structured syntax tree for further processing
- Visualize trees with ASCII art representation
- Convert trees to a dictionary representation for serialization
- Transform expressions into Polars query expressions

## Installation

```bash
# Install from PyPI (when published)
pip install predicate-bst

# Install from source
git clone https://github.com/EvanOchsner/predicate-bst.git
cd predicate-bst
pip install -e .

# Install with development dependencies
pip install -e ".[dev]"
```

## Usage

### Basic Parsing and Visualization

```python
from predicate_bst import build_boolean_syntax_tree

# Simple expression
expression1 = '@.key1 == "value1" && @.key2 != "value2"'
tree1 = build_boolean_syntax_tree(expression1)
print(tree1)  # AND(Condition(@.key1 == "value1"), Condition(@.key2 != "value2"))

# Visualize the tree as ASCII art
print(tree1.to_ascii())
# Output:
# AND
# ├── CONDITION: @.key1 == "value1"
# └── CONDITION: @.key2 != "value2"

# Complex expression with nested operators
expression2 = '@.k1 == "v1" || (@.k2 == "v2" && (@.k3 >= 1.1 || @.k4 < 0))'
tree2 = build_boolean_syntax_tree(expression2)
print(tree2)

# Convert to dictionary for serialization
tree_dict = tree2.to_dict()
print(tree_dict)
```

### Converting to Polars Expressions

```python
from predicate_bst import convert_to_polars

# Convert a predicate directly to a Polars expression string
expression = '@.price > 100 && @.category == "electronics"'
polars_expr = convert_to_polars(expression)
print(polars_expr)
# Output: (pl.element().struct.field("price").gt(100.0)).and_(pl.element().struct.field("category").eq("electronics"))

# Use with a Polars DataFrame
import polars as pl
from predicate_bst import convert_to_polars

df = pl.DataFrame({
    "id": [1, 2, 3, 4, 5],
    "category": ["electronics", "books", "electronics", "clothing", "books"],
    "price": [120.50, 15.99, 89.99, 45.00, 9.99],
    "in_stock": [True, True, False, True, True]
})
predicate = '@.price > 100 && @.category == "electronics"'
polars_expr = convert_to_polars(predicate)

# Now evaluate the expression on your DataFrame
filtered_df = df.filter(eval(polars_expr))
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
git clone https://github.com/EvanOchsner/predicate-bst.git
cd predicate-bst

# Install development dependencies
pip install -e ".[dev]"
```

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=predicate_bst

# Or use the provided test script
./run_tests.sh
```

## License

MIT