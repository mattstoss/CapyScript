import pytest
from lib import runner
import textwrap

test_cases = [
    {
        "input": "simple.capy",
        "expected_stdout": textwrap.dedent(
            """\
            my global string
            local var from func1
            my global string
            local var from func2
            first param from func2
            my global string
            local var from func3
            first param from func3
            second param from func3
            result from func4
            """
        ),
        "expected_exception": None,
    },
]


@pytest.mark.parametrize("case", test_cases)
def test_process_data(case, capsys):
    def run_test(filepath_suffix):
        filepath = "src/lib/testdata/" + filepath_suffix
        runner.execute_file(filepath)

    if case["expected_exception"]:
        with pytest.raises(case["expected_exception"]["type"]) as excinfo:
            run_test(case["input"])
        assert str(excinfo.value) == case["expected_exception"]["message"]
    else:
        run_test(case["input"])

    captured = capsys.readouterr()
    if case["expected_stdout"]:
        assert captured.out == case["expected_stdout"]
