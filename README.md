[![License: MPL 2.0](https://img.shields.io/badge/License-MPL%202.0-brightgreen.svg)](https://opensource.org/licenses/MPL-2.0)
[![Build](https://github.com/tobywf/pytest-iterassert/workflows/Build/badge.svg?branch=master&event=push)](https://github.com/tobywf/pytest-iterassert)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

# pytest-iterassert

Have you ever wanted to use `all` or `any` in a unit test, but found the assert
message to be lacking? Do assertions on class attributes in collections almost
make you wish you were coding in Java (with a nice assertion framework)?

Then this is the [pytest](https://docs.pytest.org/en/latest/) helper for you!
[pytest-iterassert](https://github.com/tobywf/pytest-iterassert) provides
`all_match` and `any_match` to give you nice asserts.

The built-in [`any`](https://docs.python.org/3/library/functions.html#any) or
[`all`](https://docs.python.org/3/library/functions.html#all) can cause a lot of
sadness when tests fail:

```plain
    def test_generator_without_iterassert() -> None:
>       assert all(i < 1 for i in range(3))
E       assert False
E        +  where False = all(<genexpr> at 0x10221a250>)
```

`all_match` and `any_match` make debugging easy:

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
    def test_attr_of_classes_with_iterassert() -> None:
        foos = [Foo(1), Foo(2), Foo(3)]
>       assert all_match(foos, get_bar) < 3
E       assert all(9001, 9002, 9003) < 3
E        +  where all(9001, 9002, 9003) = all_match([<Foo(1)>, <Foo(2)>, <Foo(3)>], get_bar)
```

Even the test summary says it all:

``` plain
FAILED example.py::test_generator_without_iterassert - assert False
FAILED example.py::test_generator_with_iterassert - assert all(0, 1, 2) < 1
FAILED example.py::test_attr_of_classes_without_iterassert - assert False
FAILED example.py::test_attr_of_classes_with_iterassert - assert all(9001, 9002, 9003) < 3
```

[pytest-iterassert is on
PyPI](https://pypi.org/project/pytest-iterassert/), so you can simply install
via `pip install pytest-iterassert` (requires Python 3.6 or higher).

## Development

This library uses [Poetry](https://python-poetry.org/) for managing
dependencies. You just need to run `poetry install`, and it will create a
virtual environment with all developer dependencies installed.

Please run `poetry run ./lint` before submitting pull requests.

## License

This library is licensed under the Mozilla Public License Version 2.0. For more
information, see `LICENSE`.
