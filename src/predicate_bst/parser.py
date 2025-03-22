"""
Parser for converting logical statements into Boolean syntax trees.

This module provides functionality to parse logical expressions with AND, OR operators,
parentheses, and conditions into a tree structure.
"""

from enum import Enum
import re
from typing import List, Dict, Any, Optional, Tuple, Union


class NodeType(Enum):
    """Types of nodes in the Boolean syntax tree."""
    AND = "AND"
    OR = "OR"
    CONDITION = "CONDITION"


class Node:
    """Represents a node in the Boolean syntax tree."""
    def __init__(self, node_type: NodeType, value: Optional[str] = None):
        self.type = node_type
        self.value = value
        self.children = []
    
    def __str__(self) -> str:
        """String representation of the node."""
        if self.type == NodeType.CONDITION:
            return f"Condition({self.value})"
        elif self.type == NodeType.AND:
            return f"AND({', '.join(str(child) for child in self.children)})"
        elif self.type == NodeType.OR:
            return f"OR({', '.join(str(child) for child in self.children)})"
        return ""
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert the node to a dictionary representation."""
        result = {
            "type": self.type.value
        }
        
        if self.type == NodeType.CONDITION:
            result["value"] = self.value
        else:
            result["children"] = [child.to_dict() for child in self.children]
        
        return result
    
    def to_ascii(self) -> str:
        """Generate an ASCII representation of the tree with this node as root."""
        lines = []
        self._to_ascii_rec(lines, "", "", "")
        return "\n".join(lines)
    
    def _to_ascii_rec(self, lines: List[str], prefix: str, child_prefix: str, label_prefix: str) -> None:
        """Recursively build ASCII representation of the tree."""
        label = str(self.type.value)
        if self.type == NodeType.CONDITION:
            label += f": {self.value}"
        
        lines.append(f"{prefix}{label_prefix}{label}")
        
        for i, child in enumerate(self.children):
            is_last_child = i == len(self.children) - 1
            
            if is_last_child:
                new_prefix = child_prefix + "    "
                new_label_prefix = "└── "
            else:
                new_prefix = child_prefix + "│   "
                new_label_prefix = "├── "
            
            child._to_ascii_rec(lines, child_prefix, new_prefix, new_label_prefix)


class TokenType(Enum):
    """Types of tokens in the logical expression."""
    AND = "&&"
    OR = "||"
    LEFT_PAREN = "("
    RIGHT_PAREN = ")"
    CONDITION = "CONDITION"


class Token:
    """Represents a token in the logical expression."""
    def __init__(self, token_type: TokenType, value: Optional[str] = None):
        self.type = token_type
        self.value = value
    
    def __str__(self) -> str:
        """String representation of the token."""
        if self.type == TokenType.CONDITION:
            return f"Condition({self.value})"
        return str(self.type.value)


def tokenize(expression: str) -> List[Token]:
    """
    Tokenize a logical expression into a list of tokens.
    
    Args:
        expression: The logical expression to tokenize
    
    Returns:
        A list of tokens
    
    Raises:
        ValueError: If the expression is invalid or contains unbalanced quotes
    """
    tokens = []
    i = 0
    n = len(expression)
    
    while i < n:
        # Skip whitespace
        if expression[i].isspace():
            i += 1
            continue
        
        # Check for operators and parentheses
        if i + 1 < n and expression[i:i+2] == '&&':
            tokens.append(Token(TokenType.AND))
            i += 2
        elif i + 1 < n and expression[i:i+2] == '||':
            tokens.append(Token(TokenType.OR))
            i += 2
        elif expression[i] == '(':
            tokens.append(Token(TokenType.LEFT_PAREN))
            i += 1
        elif expression[i] == ')':
            tokens.append(Token(TokenType.RIGHT_PAREN))
            i += 1
        else:
            # This is a condition
            start = i
            in_quotes = False
            quote_char = None
            
            # Continue until we hit an operator or a parenthesis (ignoring those in quotes)
            while i < n:
                # Handle quoted strings
                if expression[i] in ('"', "'"):
                    if not in_quotes:
                        in_quotes = True
                        quote_char = expression[i]
                    elif expression[i] == quote_char:
                        in_quotes = False
                        quote_char = None
                
                # Check for operators and parentheses (outside quotes)
                if not in_quotes:
                    if i + 1 < n and (expression[i:i+2] == '&&' or expression[i:i+2] == '||'):
                        break
                    if expression[i] == '(' or expression[i] == ')':
                        break
                
                i += 1
            
            # Check for unbalanced quotes
            if in_quotes:
                raise ValueError(f"Unbalanced quotes in condition starting at position {start}")
            
            condition = expression[start:i].strip()
            if condition:
                tokens.append(Token(TokenType.CONDITION, condition))
    
    return tokens


def parse_expression(tokens: List[Token]) -> Node:
    """
    Parse a list of tokens into a Boolean syntax tree.
    
    Args:
        tokens: The list of tokens to parse
    
    Returns:
        The root node of the Boolean syntax tree
    
    Raises:
        ValueError: If the tokens form an invalid expression
    """
    def parse_or_expr(index: int) -> Tuple[Node, int]:
        """Parse an OR expression."""
        left, index = parse_and_expr(index)
        
        while index < len(tokens) and tokens[index].type == TokenType.OR:
            # Create OR node
            or_node = Node(NodeType.OR)
            or_node.children.append(left)
            
            # Parse right operand
            index += 1
            right, index = parse_and_expr(index)
            or_node.children.append(right)
            
            left = or_node
        
        return left, index
    
    def parse_and_expr(index: int) -> Tuple[Node, int]:
        """Parse an AND expression."""
        left, index = parse_primary(index)
        
        while index < len(tokens) and tokens[index].type == TokenType.AND:
            # Create AND node
            and_node = Node(NodeType.AND)
            and_node.children.append(left)
            
            # Parse right operand
            index += 1
            right, index = parse_primary(index)
            and_node.children.append(right)
            
            left = and_node
        
        return left, index
    
    def parse_primary(index: int) -> Tuple[Node, int]:
        """Parse a primary expression (condition or parenthesized expression)."""
        if index >= len(tokens):
            raise ValueError("Unexpected end of expression")
        
        token = tokens[index]
        
        if token.type == TokenType.LEFT_PAREN:
            # Parse expression within parentheses
            index += 1
            expr, index = parse_or_expr(index)
            
            # Expect closing parenthesis
            if index < len(tokens) and tokens[index].type == TokenType.RIGHT_PAREN:
                index += 1
                return expr, index
            else:
                raise ValueError("Expected closing parenthesis")
        
        elif token.type == TokenType.CONDITION:
            # Create condition node
            node = Node(NodeType.CONDITION, token.value)
            return node, index + 1
        
        else:
            raise ValueError(f"Unexpected token: {token.type}")
    
    if not tokens:
        raise ValueError("Empty expression")
    
    # Start parsing from the first token
    result, index = parse_or_expr(0)
    
    # Ensure all tokens were consumed
    if index != len(tokens):
        raise ValueError(f"Unexpected token at position {index}")
    
    return result


def build_boolean_syntax_tree(expression: str) -> Node:
    """
    Convert a logical statement into a Boolean syntax tree.
    
    The statement can include:
    - && (logical AND)
    - || (logical OR)
    - ( and ) (parentheses for grouping)
    - Conditions (e.g., @.foo == "value")
    
    Operator precedence: AND > OR
    
    Examples:
        >>> tree = build_boolean_syntax_tree('@.key1 == "value1" && @.key2 != "value2"')
        >>> tree.type
        NodeType.AND
        >>> [child.value for child in tree.children]
        ['@.key1 == "value1"', '@.key2 != "value2"']
        
        >>> tree = build_boolean_syntax_tree('@.k1 == "v1" || (@.k2 == "v2" && (@.k3 >= 1.1 || @.k4 < 0))')
        >>> tree.type
        NodeType.OR
    
    Args:
        expression: The logical statement to parse
    
    Returns:
        The root node of the Boolean syntax tree
    
    Raises:
        ValueError: If the expression is invalid
    """
    tokens = tokenize(expression)
    return parse_expression(tokens)


def to_polars_expr(tree: Node) -> str:
    """
    Convert a Boolean syntax tree to a Polars expression string.
    
    This function translates BST nodes into polars expression code that can be executed
    using the polars query engine. It handles field references, comparison operations,
    and logical operations.
    
    Args:
        tree: The root node of the Boolean syntax tree
        
    Returns:
        A Python code string representing a Polars expression
        
    Raises:
        ValueError: If a condition has an unsupported format or operation
    """
    if tree.type == NodeType.CONDITION:
        # Parse condition: expected format is "@.field op value"
        condition = tree.value.strip()
        
        # Match field pattern (@.field)
        field_match = re.search(r'(@\.\w+)', condition)
        if not field_match:
            raise ValueError(f"Invalid field reference in condition: {condition}")
        
        field_ref = field_match.group(1)
        field_name = field_ref.replace('@.', '')
        
        # Replace @.field with pl.element().struct.field("field")
        pl_field = f'pl.element().struct.field("{field_name}")'
        
        # Match comparison operator
        if '==' in condition:
            op_parts = condition.split('==', 1)
            op_method = '.eq'
        elif '!=' in condition:
            op_parts = condition.split('!=', 1)
            op_method = '.ne'
        elif '>=' in condition:
            op_parts = condition.split('>=', 1)
            op_method = '.ge'
        elif '<=' in condition:
            op_parts = condition.split('<=', 1)
            op_method = '.le'
        elif '>' in condition:
            op_parts = condition.split('>', 1)
            op_method = '.gt'
        elif '<' in condition:
            op_parts = condition.split('<', 1)
            op_method = '.lt'
        else:
            raise ValueError(f"Unsupported comparison operator in condition: {condition}")
        
        # Extract and format value
        value = op_parts[1].strip()
        
        # For numeric comparisons, convert to float
        if op_method in ['.gt', '.lt', '.ge', '.le']:
            # Strip quotes if present
            if (value.startswith('"') and value.endswith('"')) or (value.startswith("'") and value.endswith("'")):
                value = value[1:-1]
            
            # Try to convert to float
            try:
                float_value = float(value)
                value = str(float_value)  # Ensure proper format
            except ValueError:
                # If it's not convertible to float, use it as is
                pass
        
        # Format and return polars expression for this condition
        return f"{pl_field}{op_method}({value})"
        
    elif tree.type == NodeType.AND:
        # Convert AND node to .and_() method chain
        if not tree.children:
            raise ValueError("AND node has no children")
        
        children_exprs = [to_polars_expr(child) for child in tree.children]
        if len(children_exprs) == 1:
            return children_exprs[0]
        
        # Chain all children with .and_()
        result = children_exprs[0]
        for expr in children_exprs[1:]:
            result = f"({result}).and_({expr})"
        
        return result
        
    elif tree.type == NodeType.OR:
        # Convert OR node to .or_() method chain
        if not tree.children:
            raise ValueError("OR node has no children")
        
        children_exprs = [to_polars_expr(child) for child in tree.children]
        if len(children_exprs) == 1:
            return children_exprs[0]
        
        # Chain all children with .or_()
        result = children_exprs[0]
        for expr in children_exprs[1:]:
            result = f"({result}).or_({expr})"
        
        return result
    
    raise ValueError(f"Unsupported node type: {tree.type}")


def convert_to_polars(expression: str) -> str:
    """
    Convert a logical predicate string directly to a Polars expression string.
    
    This is a convenience function that combines parsing and conversion to Polars.
    
    Args:
        expression: The logical predicate in string form
        
    Returns:
        A Python code string representing a Polars expression
        
    Raises:
        ValueError: If the expression is invalid or contains unsupported operations
    """
    tree = build_boolean_syntax_tree(expression)
    return to_polars_expr(tree)
