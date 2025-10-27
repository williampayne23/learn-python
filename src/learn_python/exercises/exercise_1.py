from learn_python.framework import Exercise, capture_output

exercise_1a = Exercise()


@exercise_1a.test()
def print_something(solution):
    with capture_output() as captured:
        solution()
        output = captured.readouterr()
        assert output.out != "", "You need to print something"
    return "Good you printed something!"


@exercise_1a.test(name='Print "Hello World!"')
def print_right_thing(solution):
    with capture_output() as captured:
        solution()
        output = captured.readouterr()
        assert "Hello World!" in output.out, 'You need to print "Hello World!" exactly'
    return "Good you printed Hello World!"


exercise_1b = Exercise()


@exercise_1b.test(name='Print "Hello name!"')
def print_hello_name(solution):
    with capture_output() as captured:
        solution("Jess")
        output = captured.readouterr()
        assert "Hello Jess!" in output.out, 'You need to print "Hello name!"'
    return "Yay!"
