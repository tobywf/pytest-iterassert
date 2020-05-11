[![License: MPL 2.0](https://img.shields.io/badge/License-MPL%202.0-brightgreen.svg)](https://opensource.org/licenses/MPL-2.0)
[![Build](https://github.com/tobywf/pytest-iterassert/workflows/Build/badge.svg?branch=master&event=push)](https://github.com/tobywf/pytest-iterassert/actions)
[![codecov](https://codecov.io/gh/tobywf/pytest-iterassert/branch/master/graph/badge.svg)](https://codecov.io/gh/tobywf/pytest-iterassert)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

# pytest-iterassert

Have you ever wanted to use `all` or `any` in a unit test, but found the assert
message to be lacking? Do assertions on class attributes in collections almost
make you wish you were coding in Java (with a nice assertion framework)? Then
this is the [pytest](https://docs.pytest.org/en/latest/) helper for you!
[pytest-iterassert](https://github.com/tobywf/pytest-iterassert) provides
`all_match` and `any_match` to give you nice asserts.

## Examples

The built-in [`any`](https://docs.python.org/3/library/functions.html#any) or
[`all`](https://docs.python.org/3/library/functions.html#all) can cause a lot of
sadness when tests fail:

```plain
    def test_generator_without_iterassert() -> None:
>       assert all(i < 1 for i in range(3))
E       assert False
E        +  where False = all(<genexpr> at 0x10221a250>)
```

`all_match` and `any_match` make debugging easy by hoisting the comparison out,
and printing meaningful debug:

```plain
    def test_generator_with_iterassert() -> None:
>       assert all_match(range(3)) < 1
E       assert all(0, 1, 2) < 1
E        +  where all(0, 1, 2) = all_match(range(0, 3))
E        +    where range(0, 3) = range(3)
```

How about a more complex example? Asserting attributes of a class instance is
pretty common.

``` plain
    def test_attr_of_classes_without_iterassert() -> None:
        foos = [Foo(1), Foo(2), Foo(3)]
>       assert all(foo.bar < 3 for foo in foos)
E       assert False
E        +  where False = all(<genexpr> at 0x10597ca50>)
```

`iterassert` makes it easy to apply functions to the iterable, and will convince
pytest to show you the result of that function!

``` plain
    def test_attr_of_classes_with_iterassert_1() -> None:
        foos = [Foo(1), Foo(2), Foo(3)]
>       assert all_match(foos, get_bar) < 3
E       assert all(9001, 9002, 9003) < 3
E        +  where all(9001, 9002, 9003) = all_match([<Foo(1)>, <Foo(2)>, <Foo(3)>], get_bar)
```

It's also possible to run more complex checks against all items, by doing the
checking inside a function:

``` plain
    def test_attr_of_classes_with_iterassert_2() -> None:
        foos = [Foo(1), Foo(2), Foo(3)]
>       assert all_match(foos, check_bar)
E       assert all(False, False, False)
E        +  where all(False, False, False) = all_match([<Foo(1)>, <Foo(2)>, <Foo(3)>], check_bar)
```

Note in this case, much like the buildin functions, `all_match` and `any_match`
take no operator or operand.

And, if you need to incorporate more transformations, but would like to see the
intermediary items, `capture` allows for this, too:

``` plain
    def test_attr_of_classes_with_iterassert_3() -> None:
        foos = [Foo(1), Foo(2), Foo(3)]
>       assert all_match(capture(foo.bar for foo in foos), check_val)
E       assert all(False, False, False)
E        +  where all(False, False, False) = all_match([9001, 9002, 9003], check_val)
E        +    where [9001, 9002, 9003] = capture(<genexpr> at 0x1031220d0>)
```

Even the test summary says it all:

``` plain
FAILED example.py::test_generator_without_iterassert - assert False
FAILED example.py::test_generator_with_iterassert - assert all(0, 1, 2) < 1
FAILED example.py::test_attr_of_classes_without_iterassert - assert False
FAILED example.py::test_attr_of_classes_with_iterassert_1 - assert all(9001, 9002, 9003) < 3
FAILED example.py::test_attr_of_classes_with_iterassert_2 - assert all(False, False, False)
FAILED example.py::test_attr_of_classes_with_iterassert_3 - assert all(False, False, False)
```

## Installation

[pytest-iterassert is on
PyPI](https://pypi.org/project/pytest-iterassert/), so you can simply install
via `pip install pytest-iterassert` (requires Python 3.6 or higher).

(If you're really brave, you can also alias `all_match` and `any_match` to the
builtin functions on import.)

## Changelog

### [0.0.3] - 2020-05-10

* Add `capture`, and allow `all_match` and `any_match` to not take an
  operator/operand, for checks inside the mapping function

### [0.0.2] - 2020-05-07

* Initial release

## Development

This library uses [Poetry](https://python-poetry.org/) for managing
dependencies. You just need to run `poetry install`, and it will create a
virtual environment with all developer dependencies installed.

Please run `poetry run ./lint` before submitting pull requests.

## License

This library is licensed under the Mozilla Public License Version 2.0. For more
information, see `LICENSE`.
