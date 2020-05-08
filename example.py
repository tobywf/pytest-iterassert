from iterassert import all_match

def test_generator_without_iterassert() -> None:
    assert all(i < 1 for i in range(3))

def test_generator_with_iterassert() -> None:
    assert all_match(range(3)) < 1

class Foo:
    def __init__(self, bar: int):
        self._bar = bar
    @property
    def bar(self) -> int:
        return self._bar + 9000
    def __repr__(self) -> str:
        return f"<Foo({self._bar})>"

def get_bar(foo: Foo) -> int:
    return foo.bar

def test_attr_of_classes_without_iterassert() -> None:
    foos = [Foo(1), Foo(2), Foo(3)]
    assert all(foo.bar < 3 for foo in foos)

def test_attr_of_classes_with_iterassert() -> None:
    foos = [Foo(1), Foo(2), Foo(3)]
    assert all_match(foos, get_bar) < 3
