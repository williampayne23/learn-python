from textwrap import dedent
from learn_python.framework._capture import capture_output
from learn_python.framework._exercise import Exercise

FIZZ_BUZZ_A_DESC = dedent("""
    Write a function that takes a number N as input and prints the numbers from 1 to N inclusive,
    but for multiples of three print "Fizz" instead of the number and for the multiples of five
    print "Buzz". For numbers which are multiples of both three and five print "FizzBuzz".

    For example, for N = 15, the output should be:
    1
    2
    Fizz
    4
    Buzz
    Fizz
    7
    8
    Fizz
    Buzz
    11
    Fizz
    13
    14
    FizzBuzz
""")


def my_fizz_buzz_per_line(line_n):
    if line_n % 3 == 0 and line_n % 5 == 0:
        return "FizzBuzz"

    if line_n % 3 == 0:
        return "Fizz"

    if line_n % 5 == 0:
        return "Buzz"

    return f"{line_n}"


def example_fizz_buzz(n):
    for i in range(1, n + 1):
        print(my_fizz_buzz_per_line(i))


ex_fizz_buzz_a = Exercise("fizz_buzz", FIZZ_BUZZ_A_DESC, example_fizz_buzz)


@ex_fizz_buzz_a.test(name="FizzBuzz")
def fizz_buzz(solution):
    with capture_output() as capsys:
        solution(15)
        result = capsys.readouterr().out
    lines = result.split("\n")[:-1]
    assert len(lines) == 15, "You need to print N lines"
    for i, line in enumerate(lines):
        target = my_fizz_buzz_per_line(i + 1)
        assert line == target, f"Line {i + 1} is {line} it shuould be {target}"
    return "Yay! FizzBuzz works!"
