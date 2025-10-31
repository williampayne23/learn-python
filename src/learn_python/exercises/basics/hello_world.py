from learn_python.framework import Exercise, capture_output

ex_hello_world_a = Exercise(
    "hello_world",
    "Write a function that prints 'Hello World!'",
    lambda: print("Hello World!"),
)


@ex_hello_world_a.test()
def print_something(solution):
    with capture_output() as captured:
        solution()
        output = captured.readouterr()
        assert output.out != "", "You need to print something"
    return "Good you printed something!"


@ex_hello_world_a.test(name='Print "Hello World!"')
def print_right_thing(solution):
    with capture_output() as captured:
        solution()
        output = captured.readouterr()
        assert "Hello World!" in output.out, 'You need to print "Hello World!" exactly'
    return "Good you printed Hello World!"


ex_hello_world_b = Exercise(
    "hello_name",
    "Write a function that takes a name as input and prints 'Hello name!'",
    lambda name: print(f"Hello {name}!"),
)


@ex_hello_world_b.test(name='Print "Hello name!"')
def print_hello_name(solution):
    with capture_output() as captured:
        solution("Name")
        output = captured.readouterr()
        assert "Hello Name!" in output.out, 'You need to print "Hello name!"'
    return "Yay!"
