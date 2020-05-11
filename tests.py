# pylint: disable=redefined-outer-name
from typing import Any, Callable

import pytest  # type: ignore

from iterassert import BaseProxy

OPERATIONS = ["==", "!=", "<", "<=", ">", ">="]
MatchOnlyTest = Callable[[str], Any]
MatchMapTest = Callable[[str, str], Any]


@pytest.fixture
def match_only_test(testdir: Any) -> MatchOnlyTest:
    def _match_only_test(assert_expr: str) -> Any:
        testdir.makepyfile(
            "from iterassert import all_match, any_match\n"
            "def test_case():\n"
            f"    assert {assert_expr}\n"
        )
        return testdir.runpytest()

    return _match_only_test


@pytest.fixture
def match_map_test(testdir: Any) -> MatchMapTest:
    def _match_map_test(assert_expr: str, map_fn_expr: str) -> Any:
        testdir.makepyfile(
            "from iterassert import all_match, any_match, capture\n"
            "def map_fn(value):\n"
            f"    return {map_fn_expr}\n"
            "def test_case():\n"
            f"    assert {assert_expr}\n"
        )
        return testdir.runpytest()

    return _match_map_test


@pytest.mark.parametrize("operation", OPERATIONS)
def test_all_match_operator_fail(
    match_only_test: MatchOnlyTest, operation: str
) -> None:
    result = match_only_test(f"all_match(range(3)) {operation} 1")
    result.assert_outcomes(failed=1)
    result.stdout.fnmatch_lines("*all(0, 1, 2)*")


def test_any_match_operator_fail(match_only_test: MatchOnlyTest) -> None:
    result = match_only_test("any_match(range(3)) == 4")
    result.assert_outcomes(failed=1)
    result.stdout.fnmatch_lines("*any(0, 1, 2)*")


def test_all_match_operator_pass(match_only_test: MatchOnlyTest) -> None:
    result = match_only_test("all_match(range(3)) < 3")
    result.assert_outcomes(passed=1)


def test_any_match_operator_pass(match_only_test: MatchOnlyTest) -> None:
    result = match_only_test("any_match(range(3)) < 3")
    result.assert_outcomes(passed=1)


def test_all_match_standalone_fail(match_only_test: MatchOnlyTest) -> None:
    result = match_only_test("all_match(range(3))")
    result.assert_outcomes(failed=1)
    result.stdout.fnmatch_lines("*all(0, 1, 2)*")


def test_any_match_standalone_fail(match_only_test: MatchOnlyTest) -> None:
    result = match_only_test("any_match([0, False, None])")
    result.assert_outcomes(failed=1)
    result.stdout.fnmatch_lines("*any(0, False, None)*")


def test_all_match_standalone_pass(match_only_test: MatchOnlyTest) -> None:
    result = match_only_test("all_match(range(1, 4))")
    result.assert_outcomes(passed=1)


def test_any_match_standalone_pass(match_only_test: MatchOnlyTest) -> None:
    result = match_only_test("any_match(range(3))")
    result.assert_outcomes(passed=1)


def test_any_match_mapping_standalone_fail(match_map_test: MatchMapTest) -> None:
    result = match_map_test("any_match(capture([0, False, None]), map_fn)", "value")
    result.assert_outcomes(failed=1)
    result.stdout.fnmatch_lines("*[[]0, False, None[]] = capture*")
    result.stdout.fnmatch_lines("*any(0, False, None)*")


def test_all_match_mapping_operator_fail(match_map_test: MatchMapTest) -> None:
    result = match_map_test(
        "all_match(capture(range(3)), map_fn) > 9000", "value + 9000"
    )
    result.assert_outcomes(failed=1)
    result.stdout.fnmatch_lines("*[[]0, 1, 2[]] = capture*")
    result.stdout.fnmatch_lines("*all(9000, 9001, 9002)*")


@pytest.mark.parametrize("operation", OPERATIONS)
def test_all_match_empty(match_only_test: MatchOnlyTest, operation: str) -> None:
    result = match_only_test(f"all_match([]) {operation} 1")
    # all([]) is True
    result.assert_outcomes(passed=1)


@pytest.mark.parametrize(
    "iterable", ["[]", "set()", "{}", '""', "(_ for _ in [])", "tuple()"]
)
def test_any_match_empty(match_only_test: MatchOnlyTest, iterable: str) -> None:
    result = match_only_test(f"any_match({iterable}) == 1")
    result.assert_outcomes(failed=1)
    result.stdout.fnmatch_lines("*any()*")


def test_base_proxy_borks() -> None:
    proxy = BaseProxy(list(range(3)))
    with pytest.raises(NotImplementedError):
        bool(proxy)


def test_rename_fail(testdir: Any) -> None:
    testdir.makepyfile(
        """
        from iterassert import any_match as any, all_match as all, capture
        def map_fn(val):
            return val > 0
        def test_case():
            assert all(capture(range(3)), map_fn)
        """
    )
    result = testdir.runpytest()
    result.assert_outcomes(failed=1)
    result.stdout.fnmatch_lines("*[[]0, 1, 2[]] = capture*")
    result.stdout.fnmatch_lines("*all(False, True, True)*")
