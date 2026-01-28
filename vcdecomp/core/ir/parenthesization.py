"""
Smart parenthesization for C expressions based on operator precedence.

This module provides intelligent parenthesis placement that follows C operator
precedence rules, avoiding redundant parentheses while maintaining correctness.
"""

from enum import Enum, auto
from dataclasses import dataclass
from typing import Optional


class ExpressionContext(Enum):
    """Context where an expression appears - affects parenthesization needs."""
    IN_CONDITION = auto()      # if/while condition: if (expr)
    IN_ASSIGNMENT = auto()     # Right side of assignment: x = expr
    IN_ARGUMENT = auto()       # Function argument: func(expr)
    IN_ARRAY_INDEX = auto()    # Array subscript: arr[expr]
    IN_RETURN = auto()         # Return statement: return expr
    IN_EXPRESSION = auto()     # General expression context
    STANDALONE = auto()        # Top-level statement


class Associativity(Enum):
    """Operator associativity for precedence resolution."""
    LEFT = auto()
    RIGHT = auto()
    NONE = auto()


@dataclass
class OperatorInfo:
    """Information about a C operator."""
    precedence: int          # Higher = tighter binding (multiplication > addition)
    associativity: Associativity
    arity: int              # 1=unary, 2=binary, 3=ternary
    is_comparison: bool = False
    is_logical: bool = False
    is_arithmetic: bool = False


# C Operator Precedence Table (from C standard)
# Higher precedence number = tighter binding
# Reference: https://en.cppreference.com/w/c/language/operator_precedence
OPERATOR_PRECEDENCE = {
    # Precedence 1 (highest) - Postfix operators
    '[]': OperatorInfo(1, Associativity.LEFT, 2),
    '()': OperatorInfo(1, Associativity.LEFT, 2),  # Function call
    '.': OperatorInfo(1, Associativity.LEFT, 2),
    '->': OperatorInfo(1, Associativity.LEFT, 2),
    '++post': OperatorInfo(1, Associativity.LEFT, 1),  # x++
    '--post': OperatorInfo(1, Associativity.LEFT, 1),  # x--

    # Precedence 2 - Prefix/unary operators
    '++pre': OperatorInfo(2, Associativity.RIGHT, 1),  # ++x
    '--pre': OperatorInfo(2, Associativity.RIGHT, 1),  # --x
    '!': OperatorInfo(2, Associativity.RIGHT, 1, is_logical=True),
    '~': OperatorInfo(2, Associativity.RIGHT, 1),
    '+unary': OperatorInfo(2, Associativity.RIGHT, 1),
    '-unary': OperatorInfo(2, Associativity.RIGHT, 1),
    '*deref': OperatorInfo(2, Associativity.RIGHT, 1),  # Dereference
    '&addr': OperatorInfo(2, Associativity.RIGHT, 1),   # Address-of
    'sizeof': OperatorInfo(2, Associativity.RIGHT, 1),

    # Precedence 3 - Type cast (not used in decompiler output currently)
    'cast': OperatorInfo(3, Associativity.RIGHT, 1),

    # Precedence 4 - Multiplicative
    '*': OperatorInfo(4, Associativity.LEFT, 2, is_arithmetic=True),
    '/': OperatorInfo(4, Associativity.LEFT, 2, is_arithmetic=True),
    '%': OperatorInfo(4, Associativity.LEFT, 2, is_arithmetic=True),

    # Precedence 5 - Additive
    '+': OperatorInfo(5, Associativity.LEFT, 2, is_arithmetic=True),
    '-': OperatorInfo(5, Associativity.LEFT, 2, is_arithmetic=True),

    # Precedence 6 - Bitwise shift
    '<<': OperatorInfo(6, Associativity.LEFT, 2),
    '>>': OperatorInfo(6, Associativity.LEFT, 2),

    # Precedence 7 - Relational
    '<': OperatorInfo(7, Associativity.LEFT, 2, is_comparison=True),
    '<=': OperatorInfo(7, Associativity.LEFT, 2, is_comparison=True),
    '>': OperatorInfo(7, Associativity.LEFT, 2, is_comparison=True),
    '>=': OperatorInfo(7, Associativity.LEFT, 2, is_comparison=True),

    # Precedence 8 - Equality
    '==': OperatorInfo(8, Associativity.LEFT, 2, is_comparison=True),
    '!=': OperatorInfo(8, Associativity.LEFT, 2, is_comparison=True),

    # Precedence 9 - Bitwise AND
    '&': OperatorInfo(9, Associativity.LEFT, 2),

    # Precedence 10 - Bitwise XOR
    '^': OperatorInfo(10, Associativity.LEFT, 2),

    # Precedence 11 - Bitwise OR
    '|': OperatorInfo(11, Associativity.LEFT, 2),

    # Precedence 12 - Logical AND
    '&&': OperatorInfo(12, Associativity.LEFT, 2, is_logical=True),

    # Precedence 13 - Logical OR
    '||': OperatorInfo(13, Associativity.LEFT, 2, is_logical=True),

    # Precedence 14 - Ternary conditional
    '?:': OperatorInfo(14, Associativity.RIGHT, 3),

    # Precedence 15 - Assignment operators (lowest precedence)
    '=': OperatorInfo(15, Associativity.RIGHT, 2),
    '+=': OperatorInfo(15, Associativity.RIGHT, 2),
    '-=': OperatorInfo(15, Associativity.RIGHT, 2),
    '*=': OperatorInfo(15, Associativity.RIGHT, 2),
    '/=': OperatorInfo(15, Associativity.RIGHT, 2),
    '%=': OperatorInfo(15, Associativity.RIGHT, 2),
    '<<=': OperatorInfo(15, Associativity.RIGHT, 2),
    '>>=': OperatorInfo(15, Associativity.RIGHT, 2),
    '&=': OperatorInfo(15, Associativity.RIGHT, 2),
    '^=': OperatorInfo(15, Associativity.RIGHT, 2),
    '|=': OperatorInfo(15, Associativity.RIGHT, 2),

    # Precedence 16 - Comma operator (lowest)
    ',': OperatorInfo(16, Associativity.LEFT, 2),
}


def get_operator_info(operator: str) -> Optional[OperatorInfo]:
    """Get precedence info for an operator."""
    return OPERATOR_PRECEDENCE.get(operator)


def is_simple_expression(expr: str) -> bool:
    """
    Check if expression is simple enough to not need parentheses.

    Simple expressions:
    - Identifiers: variable, gVar, local_123
    - Literals: 123, 0.5f, "string"
    - Field access: obj.field, ptr->field
    - Array access: arr[index]
    - Function calls: func(args)
    """
    if not expr or not expr.strip():
        return False

    expr = expr.strip()

    # Expressions with comparison/logical operators are not simple.
    if any(op in expr for op in ("==", "!=", "<=", ">=", "<", ">", "&&", "||")):
        return False

    # Literal number
    if expr.replace('.', '').replace('f', '').replace('-', '').isdigit():
        return True

    # String literal
    if expr.startswith('"') and expr.endswith('"'):
        return True

    # Function call: identifier followed by (...)
    if '(' in expr:
        paren_pos = expr.find('(')
        if paren_pos > 0 and expr.endswith(')'):
            # Check if name before paren is valid identifier
            name_part = expr[:paren_pos]
            if name_part.replace('_', '').isalnum():
                return True

    # Field access or array access
    if '->' in expr or '.' in expr or '[' in expr:
        # These have highest precedence, so they're "simple"
        return True

    # Simple identifier (no operators)
    # Allow underscores, alphanumeric
    if expr.replace('_', '').isalnum():
        return True

    return False


def needs_parens_in_condition(expr: str, operator: Optional[str] = None) -> bool:
    """
    Check if expression needs parentheses when used in if/while condition.

    Args:
        expr: The expression string
        operator: The operator used in this expression (if known)

    Returns:
        True if parentheses are needed, False otherwise
    """
    # Simple expressions never need parens in conditions
    if is_simple_expression(expr):
        return False

    # Expression already has outer parentheses
    if expr.startswith('(') and expr.endswith(')'):
        # Check if these are the "outer" parens (not function call)
        # Count parens to see if they match
        depth = 0
        for i, ch in enumerate(expr):
            if ch == '(':
                depth += 1
            elif ch == ')':
                depth -= 1
            if depth == 0 and i < len(expr) - 1:
                # Found matching close paren before end - not outer parens
                break
        else:
            # Parens match and cover whole expression
            return False

    # Comparison operators don't need extra parens in conditions
    # if (a > b) is fine, no need for if ((a > b))
    if operator and operator in ('==', '!=', '<', '<=', '>', '>='):
        return False

    # Logical operators don't need extra parens
    # if (a && b) is fine
    if operator and operator in ('&&', '||', '!'):
        return False

    # Arithmetic operators in conditions should have parens for clarity
    # if ((a + b) != 0) - outer parens around comparison, inner around arithmetic
    # But this is handled by the comparison case above

    # Default: need parens
    return True


def needs_parens(
    child_expr: str,
    child_operator: Optional[str],
    parent_operator: Optional[str],
    context: ExpressionContext,
    is_left_operand: bool = True
) -> bool:
    """
    Determine if child expression needs parentheses when used in parent context.

    Args:
        child_expr: The child expression string
        child_operator: Operator used in child expression (None if not an operator expr)
        parent_operator: Operator in parent expression (None if no parent operator)
        context: Where this expression appears
        is_left_operand: True if child is left operand of parent (affects associativity)

    Returns:
        True if parentheses are needed around child_expr, False otherwise
    """
    # Special handling for condition context
    if context == ExpressionContext.IN_CONDITION:
        return needs_parens_in_condition(child_expr, child_operator)

    # Simple expressions never need parens
    if is_simple_expression(child_expr):
        return False

    # No parent operator = top level, no parens needed
    if parent_operator is None:
        return False

    # No child operator = not an operator expression, probably doesn't need parens
    if child_operator is None:
        # But if expression contains operators (detected by spaces/symbols), might need parens
        if any(op in child_expr for op in ['+', '-', '*', '/', '&', '|', '^', '&&', '||']):
            return True
        return False

    # Get operator info
    child_info = get_operator_info(child_operator)
    parent_info = get_operator_info(parent_operator)

    if not child_info or not parent_info:
        # Unknown operator, be conservative
        return True

    # Higher precedence = tighter binding = fewer parens needed
    # If child has higher precedence than parent, no parens needed
    if child_info.precedence < parent_info.precedence:
        return False

    # If child has lower precedence, needs parens
    if child_info.precedence > parent_info.precedence:
        return True

    # Same precedence - check associativity
    if child_info.precedence == parent_info.precedence:
        if parent_info.associativity == Associativity.LEFT:
            # Left associative: a + b + c = (a + b) + c
            # Right operand needs parens, left doesn't
            return not is_left_operand
        elif parent_info.associativity == Associativity.RIGHT:
            # Right associative: a = b = c means a = (b = c)
            # Left operand needs parens, right doesn't
            return is_left_operand
        else:
            # No associativity - need parens for clarity
            return True

    return False


def wrap_if_needed(expr: str, needs_wrapping: bool) -> str:
    """
    Wrap expression in parentheses if needed.

    Args:
        expr: Expression to potentially wrap
        needs_wrapping: Whether wrapping is needed

    Returns:
        Expression with or without parentheses
    """
    if needs_wrapping:
        return f"({expr})"
    return expr
