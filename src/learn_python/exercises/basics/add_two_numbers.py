from textwrap import dedent
from learn_python.framework._capture import capture_output
from learn_python.framework._exercise import Exercise


ADD_TWO_NUMBERS_A_DESC = dedent("""
    Write a function that takes two numbers as input and prints their sum.
""")

ADD_TWO_NUMBERS_B_DESC = dedent("""
    Write a function that takes two numbers as input and returns their sum.
""")

ex_add_two_numbers_a = Exercise(
    "sum_two_numbers", ADD_TWO_NUMBERS_A_DESC, lambda a, b: print(a + b)
)
ex_add_two_numbers_b = Exercise(
    "sum_two_numbers_ret", ADD_TWO_NUMBERS_B_DESC, lambda a, b: a + b
)

testdata = [(10, 2, 12), (9, 1, 10), (2, -2, 0), (1, -2, -1), (102, 2990, 102 + 2990)]


@ex_add_two_numbers_a.parametrize("a,b,expected", testdata)
@ex_add_two_numbers_a.test(name="Add two numbers")
def test_add_two_numbers(a, b, expected, solution):
    with capture_output() as captured:
        solution(a, b)
        result = captured.readouterr().out
    assert result != "", "You haven't printed anything"
    try:
        result = int(result)
    except Exception:
        assert False, f"Got {result} which isn't a number!"
    assert result == expected, f"{a} + {b} = {expected} got {result}"
    return "Yay!"


@ex_add_two_numbers_b.parametrize("a,b,expected", testdata)
@ex_add_two_numbers_b.test(name="Add two numbers")
def test_add_two_numbers_ret(a, b, expected, solution):
    result = solution(a, b)
    assert result is not None, "You haven't returned anything"
    assert result == expected, f"{a} + {b} = {expected} got {result}"
    return "Yay!"
