# pylint: disable=redefined-outer-name
from typing import Any, Callable

import pytest  # type: ignore

from iterassert import BaseCapture

OPERATIONS = ["==", "!=", "<", "<=", ">", ">="]
TestFactory = Callable[[str], Any]


@pytest.fixture
def test_factory(testdir: Any) -> TestFactory:
    def _test_factory(assert_expr: str) -> Any:
        testdir.makepyfile(
            "from iterassert import all_match, any_match\n"
            "def test_case():\n"
            f"    assert {assert_expr}\n"
        )
        return testdir.runpytest()

    return _test_factory


@pytest.mark.parametrize("operation", OPERATIONS)
def test_all_match_identity(test_factory: TestFactory, operation: str) -> None:
    result = test_factory(f"all_match(range(3)) {operation} 1")
    result.assert_outcomes(failed=1)
    result.stdout.fnmatch_lines("*all(0, 1, 2)*")


def test_any_match_identity(test_factory: TestFactory) -> None:
    result = test_factory("any_match(range(3)) == 4")
    result.assert_outcomes(failed=1)
    result.stdout.fnmatch_lines("*any(0, 1, 2)*")


def test_any_match_mapping(testdir: Any) -> None:
    testdir.makepyfile(
        """
        from iterassert import any_match
        def mapping(val):
            return val + 1
        def test_case():
            assert any_match(range(3), mapping) == 4
        """
    )
    result = testdir.runpytest()
    result.assert_outcomes(failed=1)
    result.stdout.fnmatch_lines("*any(1, 2, 3)*")


@pytest.mark.parametrize("operation", OPERATIONS)
def test_all_match_empty(test_factory: TestFactory, operation: str) -> None:
    result = test_factory(f"all_match([]) {operation} 1")
    # all([]) is True
    result.assert_outcomes(passed=1)


@pytest.mark.parametrize(
    "iterable", ["[]", "set()", "{}", '""', "(_ for _ in [])", "tuple()"]
)
def test_any_match_empty(test_factory: TestFactory, iterable: str) -> None:
    result = test_factory(f"any_match({iterable}) == 1")
    result.assert_outcomes(failed=1)
    result.stdout.fnmatch_lines("*any()*")


def test_base_capture_borks() -> None:
    capture = BaseCapture(list(range(3)))
    with pytest.raises(NotImplementedError):
        capture == 1  # pylint: disable=pointless-statement
