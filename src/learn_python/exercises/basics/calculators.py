from textwrap import dedent
from learn_python.framework._exercise import Exercise

CREATE_CALCULATOR_INSTRUCTIONS = dedent("""
    Create a function that acts as a simple calculator.
    The function should take three parameters:
    - operation: A string that can be "+", "-", "*", or "/"
    - a: The first number (int or float)
    - b: The second number (int or float)
    The function should return the result of applying the operation to the two numbers.
""")


def example_calculator(op, a, b):
    if op == "+":
        return a + b
    elif op == "-":
        return a - b
    elif op == "*":
        return a * b
    elif op == "/":
        return a / b
    else:
        raise ValueError(f"Unknown operation {op}")


ex_calculator_a = Exercise(
    "make_a_calculator", CREATE_CALCULATOR_INSTRUCTIONS, example_calculator
)

add_data = [(10, 2, 12), (9, 1, 10), (2, -2, 0), (1, -2, -1), (102, 2990, 102 + 2990)]
sub_data = [(10, 2, 8), (9, 1, 8), (2, -2, 4), (1, -2, 3), (102, 2990, 102 - 2990)]

mult_data = [(2, 2, 4), (4, 4, 16), (3, -1, -3), (-2, -3, 6), (2, 0.5, 1)]

div_data = [(2, 2, 1), (4, 2, 2), (2, 4, 0.5), (2, 0.1, 20)]


@ex_calculator_a.parametrize("a,b,expected", add_data)
@ex_calculator_a.test(name="Can add")
def can_add(a, b, expected, solution):
    result = solution("+", a, b)
    assert result is not None, "You haven't returned anything"
    assert result == expected, f"{a} + {b} = {expected} got {result}"
    return "Your calculator can add numbers"


@ex_calculator_a.parametrize("a,b,expected", sub_data)
@ex_calculator_a.test(name="Can subtract")
def can_subtract(a, b, expected, solution):
    result = solution("-", a, b)
    assert result is not None, "You haven't returned anything"
    assert result == expected, f"{a} - {b} = {expected} got {result}"
    return "Your calculator can subtract numbers"


@ex_calculator_a.parametrize("a,b,expected", mult_data)
@ex_calculator_a.test(name="Can multiply")
def can_mult(a, b, expected, solution):
    result = solution("*", a, b)
    assert result is not None, "You haven't returned anything"
    assert result == expected, f"{a} * {b} = {expected} got {result}"
    return "Your calculator can multiply numbers"


@ex_calculator_a.parametrize("a,b,expected", div_data)
@ex_calculator_a.test(name="Can divide")
def can_divide(a, b, expected, solution):
    result = solution("/", a, b)
    assert result is not None, "You haven't returned anything"
    assert result == expected, f"{a} / {b} = {expected} got {result}"
    return "Your calculator can divide numbers"
