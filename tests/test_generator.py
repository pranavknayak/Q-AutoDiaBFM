import ast
import sys
from typing import Set

sys.path.insert(0, "../src")
from qiskit_flake8 import Plugin


def _results(s: str) -> Set[str]:
    tree = ast.parse(s)
    plugin = Plugin(tree)
    return {f'{line}:{col + 1} {msg}' for line, col, msg, _ in plugin.run()}


def test_trivial_case():
    assert _results('') == set()


def test_incorrect_named_arguments():
    ret = _results('f(**{"foo": "bar"})')
    assert ret == {'1:1 QKF100 all arguments in ** are identifiers', '1:1 QKF101 all arguments in ** are identifiers'}


def test_allowed_splat_arguments():
    assert _results('f(**{"foo-bar": "baz"})') == set()