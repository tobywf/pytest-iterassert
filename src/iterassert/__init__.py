import operator
from typing import Any, Callable, Iterable, Optional, Sequence


class BaseCapture:
    NAME = "invalid"

    @staticmethod
    def _assert_fn(_iterable: Iterable[bool]) -> bool:
        raise NotImplementedError()

    def __init__(self, values: Sequence[Any]):
        self._values = values

    def __repr__(self) -> str:
        """Since the capture is returned, this is what pytest will use to expand/print
        the assert info.
        """
        joined = ", ".join(repr(value) for value in self._values)
        return f"{self.NAME}({joined})"

    def _apply(self, operator_fn: Callable[[Any, Any], bool], other: Any) -> bool:
        return self._assert_fn(operator_fn(value, other) for value in self._values)

    def __lt__(self, other: Any) -> bool:
        return self._apply(operator.lt, other)

    def __le__(self, other: Any) -> bool:
        return self._apply(operator.le, other)

    def __eq__(self, other: Any) -> bool:
        return self._apply(operator.eq, other)

    def __ne__(self, other: Any) -> bool:
        return self._apply(operator.ne, other)

    def __gt__(self, other: Any) -> bool:
        return self._apply(operator.gt, other)

    def __ge__(self, other: Any) -> bool:
        return self._apply(operator.ge, other)


class AllCapture(BaseCapture):
    NAME = "all"
    _assert_fn = all  # type: ignore


class AnyCapture(BaseCapture):
    NAME = "any"
    _assert_fn = any  # type: ignore


def identity(value: Any) -> Any:
    return value


def all_match(
    values: Iterable[Any], function: Callable[[Any], Any] = identity
) -> AllCapture:
    return AllCapture([function(value) for value in values])


def any_match(
    values: Iterable[Any], function: Callable[[Any], Any] = identity
) -> AnyCapture:
    return AnyCapture([function(value) for value in values])


__all__ = ["all_match", "any_match"]
