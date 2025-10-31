from textwrap import dedent
from learn_python.framework._exercise import Exercise

FIBBONACI_DESC = dedent("""
    Write a function that takes a number N as input and returns the Nth number in the
    Fibbonaci sequence. Where the Fibbonaci sequence is defined as:
    F(0) = 0
    F(1) = 1
    F(N) = F(N-1) + F(N-2) for N > 1
""")


def ex_fibbonaci(n):
    if n <= 1:
        return n

    # Only keep track of last two values
    prev2 = 0
    prev1 = 1

    for i in range(2, n + 1):
        current = prev1 + prev2
        prev2 = prev1
        prev1 = current
    return prev1


exercise_5 = Exercise("fibbonaci", FIBBONACI_DESC, ex_fibbonaci)


lengths_to_check = [
    10,
    40,
    50,
]


@exercise_5.parametrize("N", lengths_to_check)
@exercise_5.test(name="Fibbonaci?")
def test_fibbonaci(solution, N):
    theirs = solution(N)
    mine = ex_fibbonaci(N)
    assert theirs == mine, f"fib({N}) = {mine}, but you got {theirs}"
    return "Fibbonaci!"
