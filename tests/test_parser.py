"""Tests for the predicate_to_bst package."""

import pytest
from predicate_to_bst.parser import (
    NodeType,
    Node,
    TokenType,
    Token,
    tokenize,
    parse_expression,
    build_boolean_syntax_tree
)


def test_tokenize_simple_condition():
    """Test tokenizing a simple condition."""
    expression = '@.key == "value"'
    tokens = tokenize(expression)
    assert len(tokens) == 1
    assert tokens[0].type == TokenType.CONDITION
    assert tokens[0].value == '@.key == "value"'


def test_tokenize_and_expression():
    """Test tokenizing an AND expression."""
    expression = '@.key1 == "value1" && @.key2 != "value2"'
    tokens = tokenize(expression)
    assert len(tokens) == 3
    assert tokens[0].type == TokenType.CONDITION
    assert tokens[0].value == '@.key1 == "value1"'
    assert tokens[1].type == TokenType.AND
    assert tokens[2].type == TokenType.CONDITION
    assert tokens[2].value == '@.key2 != "value2"'


def test_tokenize_complex_expression():
    """Test tokenizing a complex expression with nested operators and parentheses."""
    expression = '@.k1 == "v1" || (@.k2 == "v2" && (@.k3 >= 1.1 || @.k4 < 0))'
    tokens = tokenize(expression)
    assert len(tokens) == 11
    assert tokens[0].type == TokenType.CONDITION
    assert tokens[0].value == '@.k1 == "v1"'
    assert tokens[1].type == TokenType.OR
    assert tokens[2].type == TokenType.LEFT_PAREN
    assert tokens[3].type == TokenType.CONDITION
    assert tokens[3].value == '@.k2 == "v2"'
    assert tokens[4].type == TokenType.AND
    assert tokens[5].type == TokenType.LEFT_PAREN
    assert tokens[6].type == TokenType.CONDITION
    assert tokens[6].value == '@.k3 >= 1.1'
    assert tokens[7].type == TokenType.OR
    assert tokens[8].type == TokenType.CONDITION
    assert tokens[8].value == '@.k4 < 0'
    assert tokens[9].type == TokenType.RIGHT_PAREN
    assert tokens[10].type == TokenType.RIGHT_PAREN


def test_tokenize_with_quoted_strings():
    """Test that operators and parentheses inside quotes don't affect tokenization."""
    expression = '@.key == "value with && and || inside"'
    tokens = tokenize(expression)
    assert len(tokens) == 1
    assert tokens[0].type == TokenType.CONDITION
    assert tokens[0].value == '@.key == "value with && and || inside"'


def test_build_tree_simple_condition():
    """Test building a tree from a simple condition."""
    expression = '@.price > 150.35'
    tree = build_boolean_syntax_tree(expression)
    assert tree.type == NodeType.CONDITION
    assert tree.value == '@.price > 150.35'


def test_build_tree_and_expression():
    """Test building a tree from an AND expression."""
    expression = '@.key1 == "value1" && @.key2 != "value2"'
    tree = build_boolean_syntax_tree(expression)
    assert tree.type == NodeType.AND
    assert len(tree.children) == 2
    assert tree.children[0].type == NodeType.CONDITION
    assert tree.children[0].value == '@.key1 == "value1"'
    assert tree.children[1].type == NodeType.CONDITION
    assert tree.children[1].value == '@.key2 != "value2"'


def test_build_tree_complex_expression():
    """Test building a tree from a complex expression with nested operators."""
    expression = '@.k1 == "v1" || (@.k2 == "v2" && (@.k3 >= 1.1 || @.k4 < 0))'
    tree = build_boolean_syntax_tree(expression)
    assert tree.type == NodeType.OR
    assert len(tree.children) == 2
    assert tree.children[0].type == NodeType.CONDITION
    assert tree.children[0].value == '@.k1 == "v1"'
    assert tree.children[1].type == NodeType.AND
    assert len(tree.children[1].children) == 2
    assert tree.children[1].children[0].type == NodeType.CONDITION
    assert tree.children[1].children[0].value == '@.k2 == "v2"'
    assert tree.children[1].children[1].type == NodeType.OR
    assert len(tree.children[1].children[1].children) == 2
    assert tree.children[1].children[1].children[0].type == NodeType.CONDITION
    assert tree.children[1].children[1].children[0].value == '@.k3 >= 1.1'
    assert tree.children[1].children[1].children[1].type == NodeType.CONDITION
    assert tree.children[1].children[1].children[1].value == '@.k4 < 0'


def test_build_tree_error_handling():
    """Test error handling for invalid expressions."""
    # Test empty expression
    with pytest.raises(ValueError):
        build_boolean_syntax_tree('')
    
    # Test unbalanced parentheses
    with pytest.raises(ValueError):
        build_boolean_syntax_tree('(@.key1 == "value1"')
    
    # Test unbalanced quotes
    with pytest.raises(ValueError):
        build_boolean_syntax_tree('@.key == "unbalanced')


def test_node_to_dict():
    """Test converting a node to a dictionary representation."""
    condition_node = Node(NodeType.CONDITION, '@.key == "value"')
    condition_dict = condition_node.to_dict()
    assert condition_dict["type"] == "CONDITION"
    assert condition_dict["value"] == '@.key == "value"'

    and_node = Node(NodeType.AND)
    and_node.children = [
        Node(NodeType.CONDITION, '@.key1 == "value1"'),
        Node(NodeType.CONDITION, '@.key2 == "value2"')
    ]
    and_dict = and_node.to_dict()
    assert and_dict["type"] == "AND"
    assert len(and_dict["children"]) == 2
    assert and_dict["children"][0]["type"] == "CONDITION"
    assert and_dict["children"][0]["value"] == '@.key1 == "value1"'
    assert and_dict["children"][1]["type"] == "CONDITION"
    assert and_dict["children"][1]["value"] == '@.key2 == "value2"'


def test_node_str_representation():
    """Test string representation of nodes."""
    condition_node = Node(NodeType.CONDITION, '@.key == "value"')
    assert str(condition_node) == 'Condition(@.key == "value")'

    and_node = Node(NodeType.AND)
    and_node.children = [
        Node(NodeType.CONDITION, '@.key1 == "value1"'),
        Node(NodeType.CONDITION, '@.key2 == "value2"')
    ]
    assert str(and_node) == 'AND(Condition(@.key1 == "value1"), Condition(@.key2 == "value2"))'
